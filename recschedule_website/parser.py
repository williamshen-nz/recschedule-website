import re
from collections import defaultdict
from typing import Dict, List

from recschedule_website.types import CustomDate, Schedule

# Recommend using https://regex101.com/ for debugging

DATE_REGEX = (
    r"((Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),"
    r"\s+(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+(\d{1,2}),\s+(\d{4}))"
)
BADMINTON_REGEX = (
    r"(\d{1,2}:\d{2})\s(AM|PM)\s+(\d{1,2}:\d{2})\s(AM|PM)\s+.*Badminton\s+(.*)"
)
# For cases where the schedule spans multiple lines
OPENREC_REGEX = (
    r"(\d{1,2}:\d{2})\s(AM|PM)\s+(\d{1,2}:\d{2})\s(AM|PM)\s+.*Open Recreation -\s+(.*)"
)
SHARED_OPENREC_REGEX = (
    r"(\d{1,2}:\d{2})\s(AM|PM)\s+(\d{1,2}:\d{2})\s(AM|PM)\s+.*Open Rec \s+(.*)"
)
SHARED_OPENRECREATION_REGEX = (
    r"(\d{1,2}:\d{2})\s(AM|PM)\s+(\d{1,2}:\d{2})\s(AM|PM)\s+.*Open Recreation \s+(.*)"
)


def extract_dates(recschedule: str) -> List[CustomDate]:
    """
    Extract all the dates in the recschedule sequentially. Note that
    there may be duplicates, hence we use a list.
    """
    date_matches = re.findall(DATE_REGEX, recschedule)
    # Each match should have 5 groups
    for matches in date_matches:
        assert len(matches) == 5, f"Unexpected matches! {matches}"

    # First group contains entire date string (e.g. Monday, January 15, 2022)
    custom_dates = [CustomDate(matches[0]) for matches in date_matches]
    return custom_dates


def meet_open_rec_rule(line):
    return (("Rockwell SOUTH CT" in line) or ("Rockwell NORTH CT" in line) or ("du Pont DU PONT CT" in line)) and (
            ("Open Rec " in line) or ("Open Recreation" in line)) and ("-" not in line)


def filter_for_sport(
        date: CustomDate, substring: str, sport: str = "Badminton", include_shared_open_rec: bool = False
) -> List[Schedule]:
    # FIXME: if you want to add another sport you should alter this
    if sport != "Badminton":
        raise NotImplementedError(f"Sport {sport} not implemented")

    split_text = substring.split("\n")
    # Filter for Badminton strings
    lines = [
        line.strip()
        for idx, line in enumerate(split_text)
        if "Badminton" in line
           or (
               # Sometimes the Badminton line item is spread across 2 string
               # lines, so we explicitly check for that case
                   idx < len(split_text) - 1
                   and "Badminton" in split_text[idx + 1]
                   and "Badminton" not in line
                   and "Open Rec" in line
           )
    ]

    # Convert to Schedule objects by matching to regex
    schedules = []
    for idx, line in enumerate(lines):
        matches = re.findall(BADMINTON_REGEX, line)

        if len(matches) == 1:
            # Successful match
            matches = matches[0]
            assert len(matches) == 5
        else:
            # This indicates that the badminton schedule probably lives
            # across two lines. Let's check for that
            if line == "Rec.)                       Badminton":
                continue

            assert lines[idx + 1] == "Rec.)                       Badminton", lines[
                idx + 1
                ]

            matches = re.findall(OPENREC_REGEX, line)
            assert len(matches) == 1 and len(matches[0]) == 5
            matches = matches[0]

        start_time = matches[0] + " " + matches[1]
        end_time = matches[2] + " " + matches[3]
        location = matches[4]
        # Create Schedule for this entry
        schedules.append(Schedule(date, start_time, end_time, location, False))
    if include_shared_open_rec:
        open_rec_lines = [
            line.strip()
            for idx, line in enumerate(split_text)
            if meet_open_rec_rule(line)
        ]
        for idx, line in enumerate(open_rec_lines):
            matches = re.findall(SHARED_OPENREC_REGEX, line) if "Open Rec " in line \
                else re.findall(SHARED_OPENRECREATION_REGEX, line)
            assert len(matches) == 1
            matches = matches[0]
            assert len(matches) == 5
            start_time = matches[0] + " " + matches[1]
            end_time = matches[2] + " " + matches[3]
            location = matches[4]
            schedules.append(Schedule(date, start_time, end_time, location, True))
    return schedules


def to_key(schedule: Schedule) -> bool:
    """
    Convert schedule time to the form of ('AM/PM', hh, mm ) for sorting
    Change 12 PM to 0 PM for comparison
    In case of start time being the same, compare the end time.
    In case of both start and end time being the same, compare location
    """
    time, suffix = schedule.start_time.split()
    hh, mm = time.split(':')
    if suffix == 'PM' and hh == "12":
        hh = "0"
    result = [suffix, int(hh), int(mm)]
    time, suffix = schedule.end_time.split()
    hh, mm = time.split(':')
    if suffix == 'PM' and hh == "12":
        hh = "0"
    result += [suffix, int(hh), int(mm)]
    result += schedule.location
    return result


def get_schedules_for_dates(
        dates: List[CustomDate], recschedule: str, sport: str = "Badminton", include_shared_open_rec: bool = False
) -> Dict[CustomDate, List[Schedule]]:
    """
    Get the line items between dates that we parsed out of the recschedule.
    This is so we can process them later.

    Returns a dict mapping the date as a CustomDate to a list of strings containing the schedules
    """
    # There could be multiple occurrences of a date in the recschedule, so keep track of
    # indexes already scanned
    date_to_str_idx: Dict[CustomDate, int] = defaultdict(int)
    date_to_schedule_strs: Dict[CustomDate, List[Schedule]] = defaultdict(list)

    for idx, date in enumerate(dates):
        str_idx = recschedule.find(date.date_str, date_to_str_idx[date] + 1)

        # If we're at the second date, we can start filling in substring between
        # first date and second date
        if idx >= 1:
            prev_date = dates[idx - 1]
            prev_date_str_idx = date_to_str_idx[prev_date]

            substring = recschedule[prev_date_str_idx:str_idx]
            date_to_schedule_strs[prev_date].extend(
                filter_for_sport(date=prev_date, substring=substring, sport=sport,
                                 include_shared_open_rec=include_shared_open_rec)
            )
            if include_shared_open_rec:
                date_to_schedule_strs[prev_date].sort(key=to_key)

        # If last element of dates then process that as well
        if idx == len(dates) - 1:
            substring = recschedule[str_idx:]
            date_to_schedule_strs[date].extend(
                filter_for_sport(date=date, substring=substring, sport=sport,
                                 include_shared_open_rec=include_shared_open_rec)
            )
            if include_shared_open_rec:
                date_to_schedule_strs[date].sort(key=to_key)
        # Update index of the current date now we have processed it
        date_to_str_idx[date] = str_idx

    return date_to_schedule_strs
