from recschedule_website.parser import extract_dates, get_schedules_for_dates
from recschedule_website.website import write_html_for_schedule


def process_recschedule(
    in_fname: str, out_fname: str, include_shared_sessions: bool = True
) -> None:
    """
    Integrate the different methods together

    :param in_fname: recschedule txt file to read
    :param out_fname: name of output HTML file
    :param include_shared_sessions: whether to include shared Open Rec sessions,
        i.e., those that are not strictly Badminton but for all sports.
    :return: None
    """
    print(f"Including shared sessions: {include_shared_sessions}")
    recschedule = open(in_fname, "r").read()
    dates = extract_dates(recschedule)
    date_to_schedules = get_schedules_for_dates(
        dates, recschedule, include_shared_sessions=include_shared_sessions
    )
    write_html_for_schedule(date_to_schedules, output_html_fname=out_fname)
