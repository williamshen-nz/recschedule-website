from collections import defaultdict
from datetime import datetime, timedelta

from recschedule_website.mazevo_helpers import (
    get_badminton_schedules,
    get_mazevo_bookings,
)
from recschedule_website.utils import BOSTON_TZ
from recschedule_website.website import write_html_for_schedule


def main(out_fname: str = "index.html", include_shared_sessions: bool = True) -> None:
    """
    Main function to generate the schedule

    :param out_fname: name of output HTML file
    :param include_shared_sessions: whether to include shared Open Rec sessions,
        i.e., those that are not strictly Badminton but for all sports.
    :return: None
    """
    # Get current time in Boston timezone
    start_time = datetime.now(BOSTON_TZ).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_time = start_time + timedelta(days=7)

    print(f"Including shared sessions: {include_shared_sessions}")
    print(f"Start time: {start_time}, End time: {end_time}")

    bookings, payload = get_mazevo_bookings(start_time, end_time)
    schedules = get_badminton_schedules(
        bookings, include_shared_sessions=include_shared_sessions
    )

    date_to_schedules = defaultdict(list)
    for schedule in schedules:
        date_to_schedules[schedule.date].append(schedule)

    write_html_for_schedule(
        date_to_schedules, request_payload=payload, output_html_fname=out_fname
    )


if __name__ == "__main__":
    main()
