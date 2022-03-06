import os
from datetime import datetime
from typing import Dict, List

import pytz
from jinja2 import Template

from recschedule_website.types import BOSTON_TZ, CustomDate, Schedule


def _determine_template_fname() -> str:
    module_dir = os.path.dirname(__file__)
    assets_dir = os.path.join(module_dir, "assets")
    template_path = os.path.join(assets_dir, "template.html")
    print(template_path)
    return template_path


def _get_render_dict(
    date_to_schedules: Dict[CustomDate, List[Schedule]], debug: bool
) -> Dict:
    """Get dictionary with keys and values for rendering the Jinja template"""
    # Get current time in Boston Timezone
    current_datetime_in_boston_tz = (
        datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(BOSTON_TZ)
    )
    human_readable_date = current_datetime_in_boston_tz.strftime(
        "%a, %d %b %Y %-I:%M:%S %p"
    )

    # Past dates
    past_date_to_schedules = {
        date: schedules
        for date, schedules in date_to_schedules.items()
        if date.datetime.date() < current_datetime_in_boston_tz.date()
    }

    # Upcoming sessions
    upcoming_date_to_schedules = {
        date: schedules
        for date, schedules in date_to_schedules.items()
        if date.datetime.date() >= current_datetime_in_boston_tz.date()
    }

    # Debug print statements
    if debug:
        print(f"Current Boston time {human_readable_date}")
        print("= Past Sessions = ")
        for date, schedules in past_date_to_schedules.items():
            print(f"{date} has {len(schedules)} sessions")
        print("= Upcoming Sessions = ")
        for date, schedules in upcoming_date_to_schedules.items():
            print(f"{date} has {len(schedules)} sessions")

    # Return dict for Jinja rendering
    return {
        "current_date_str": human_readable_date,
        "past_date_to_schedules": past_date_to_schedules,
        "upcoming_date_to_schedules": upcoming_date_to_schedules,
    }


def _render_html_template(
    date_to_schedules: Dict[CustomDate, List[Schedule]], debug: bool
) -> str:
    """Load the Jinja template, get the relevant values and render it"""
    # Get File Content in String
    template_str = open(_determine_template_fname(), "r").read()
    jinja_template = Template(source=template_str)

    print("ashduioshirohrioehwiorhewior")

    # Render template
    render_dict = _get_render_dict(date_to_schedules, debug)
    html = jinja_template.render(**render_dict)
    return html


def write_html_for_schedule(
    date_to_schedules: Dict[CustomDate, List[Schedule]],
    output_html_fname: str,
    debug: bool = True,
) -> None:
    """Render Jinja template and write out to a file"""
    html = _render_html_template(date_to_schedules, debug)
    with open(output_html_fname, "w") as f:
        f.write(html)
        if debug:
            print(f"Wrote HTML to {output_html_fname}")
