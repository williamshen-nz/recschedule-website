from recschedule_website.parser import extract_dates, get_schedules_for_dates
from recschedule_website.website import write_html_for_schedule


def process_recschedule(in_fname: str, out_fname: str) -> None:
    """
    Integrate the different methods together

    :param in_fname: recschedule txt file to read
    :param out_fname: name of output HTML file
    :return: None
    """
    recschedule = open(in_fname, "r").read()
    dates = extract_dates(recschedule)
    date_to_schedules = get_schedules_for_dates(dates, recschedule)
    write_html_for_schedule(date_to_schedules, output_html_fname=out_fname)
