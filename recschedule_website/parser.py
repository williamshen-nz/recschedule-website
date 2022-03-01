import re
from collections import defaultdict
from typing import List, Dict

from recschedule_website.schedule import Schedule

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


def extract_dates(recschedule: str) -> List[str]:
    """
    Extract all the dates in the recschedule sequentially. Note that
    there may be duplicates, hence we use a list.
    """
    date_matches = re.findall(DATE_REGEX, recschedule)
    # Each match should have 5 groups
    for matches in date_matches:
        assert len(matches) == 5, f"Unexpected matches! {matches}"

    # First group contains entire date string (e.g. Monday, January 15, 2022)
    return [matches[0] for matches in date_matches]


def filter_for_sport(
    date: str, substring: str, sport: str = "Badminton"
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
        schedules.append(Schedule(date, start_time, end_time, location))

    return schedules


def get_schedules_for_dates(
    dates: List[str], recschedule: str, sport: str = "Badminton"
) -> Dict[str, List[Schedule]]:
    """
    Get the line items between dates that we parsed out of the recschedule.
    This is so we can process them later.

    Returns a dict mapping the date as a string to a list of strings containing the schedules
    """
    # There could be multiple occurrences of a date in the recschedule, so keep track of
    # indexes already scanned
    date_to_str_idx: Dict[str, int] = defaultdict(int)
    date_to_schedule_strs: Dict[str, List[Schedule]] = defaultdict(list)

    for idx, date in enumerate(dates):
        str_idx = recschedule.find(date, date_to_str_idx[date] + 1)

        # If we're at the second date, we can start filling in substring between
        # first date and second date
        if idx >= 1:
            prev_date = dates[idx - 1]
            prev_date_str_idx = date_to_str_idx[prev_date]

            substring = recschedule[prev_date_str_idx:str_idx]
            date_to_schedule_strs[prev_date].extend(
                filter_for_sport(date=prev_date, substring=substring, sport=sport)
            )

        # If last element of dates then process that as well
        if idx == len(dates) - 1:
            substring = recschedule[str_idx:]
            date_to_schedule_strs[date].extend(
                filter_for_sport(date=date, substring=substring, sport=sport)
            )

        # Update index of the current date now we have processed it
        date_to_str_idx[date] = str_idx

    return date_to_schedule_strs
