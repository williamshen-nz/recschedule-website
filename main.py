import sys

from recschedule_website.parser import extract_dates, get_schedules_for_dates
from recschedule_website.website import write_html_for_schedule


def process_recschedule(in_fname: str, out_fname: str):
    recschedule = open(in_fname, "r").read()
    dates = extract_dates(recschedule)
    date_to_schedules = get_schedules_for_dates(dates, recschedule)
    write_html_for_schedule(date_to_schedules, fname=out_fname)


if __name__ == "__main__":
    assert (
        len(sys.argv) == 3
    ), "Usage: python main.py <filename of recschedule> <output HTML filename>"
    process_recschedule(in_fname=sys.argv[1], out_fname=sys.argv[2])
