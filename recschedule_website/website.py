from datetime import datetime
from typing import Dict, List

import pytz

from recschedule_website.types import BOSTON_TZ, CustomDate, Schedule

HTML_HEAD = """
<!DOCTYPE html>

<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
<meta name="description" content="MIT Open Recreation Badminton - Unofficial Schedule">

<title>MIT Open Rec Badminton Schedule</title>

<script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');ga('create','UA-71827372-1','auto');ga('send','pageview');</script>

<link rel="icon" type="image/png" href="https://shen.nz/images/mit_logo.svg">
<link rel="stylesheet" type="text/css" href="stylesheet.css">

<!-- Open all links (i.e. Google Calendar) in new tab -->
<base target="_blank">
</head>

<body>
"""

HTML_END = """
<br>
<hr>
<p><strong>Badminton Court Guide:</strong> du Pont courts are very slippery, Rockwell is a lot better.</p>
<p><strong>Notes:</strong> this schedule is updated every 30 minutes from the latest recschedule downloaded
(<a href="https://shen.nz/badminton/recschedule-latest.pdf">https://shen.nz/badminton/recschedule-latest.pdf</a>). <br>
You can find the original recschedule at: <a href="http://web.mit.edu/athletics/www/recschedule.pdf">http://web.mit.edu/athletics/www/recschedule.pdf</a></p>
<p>There is a known issue where your browser may show you an old version of the schedule. This is probably due to client-side caching, etc.<br>
There is no guarantee for accuracy. Please contact willshen at mit.edu with any questions or issues.</p>
<p><a href="https://github.com/williamshen-nz/recschedule-website">Open Source on GitHub</a>. Feel free to contribute!</p>
</body>
</html>
"""


def write_html_for_schedule(
    date_to_schedules: Dict[CustomDate, List[Schedule]],
    out_fname: str,
    filter_dates_before_now: bool,
    debug: bool = True,
) -> None:
    """
    Form and write the HTML file for each date and its schedules.

    :param date_to_schedules: Dict of CustomDate to Schedule objects for that date
    :param out_fname: fname of output HTML file
    :param filter_dates_before_now: whether we should filter out dates before now
        (i.e., when we are running this script)
    :param debug: whether to print some debug statements
    :return: None
    """
    current_datetime_in_boston_tz = (
        datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(BOSTON_TZ)
    )

    # HTML Section
    human_readable_date = current_datetime_in_boston_tz.strftime(
        "%a, %d %b %Y %-I:%M:%S %p"
    )
    if debug:
        print(f"Current Boston time {human_readable_date}")

    if filter_dates_before_now:
        time_debug_html = (
            f"<p>Showing sessions on or after {human_readable_date} Boston time.</p>"
        )
    else:
        time_debug_html = f"<p>Last updated on {human_readable_date} Boston time.</p>"

    html_lines = [
        HTML_HEAD,
        "<h2>MIT Open Rec Badminton - Unofficial Schedule</h2>",
        time_debug_html,
        "<hr>",
    ]

    for date, schedules in date_to_schedules.items():
        # Filter out dates before now (not inclusive as today may not have ended)
        if (
            filter_dates_before_now
            and date.datetime.date() < current_datetime_in_boston_tz.date()
        ):
            if debug:
                print(f"{date} has {len(schedules)} sessions. Filtering out.")
            continue

        print(f"{date} has {len(schedules)} sessions")
        # Form HTML for each schedule
        html_lines.append(f"<p class='date'><strong>{date}</strong></p>")
        if schedules:
            for schedule in schedules:
                html_lines.append("<p>" + schedule.to_html() + "</p>")
        else:
            html_lines.append("<p>No sessions.</p>")

    html_lines.append(HTML_END)
    open(out_fname, "w").write("\n".join(html_lines))
    if debug:
        print(f"Wrote HTML to {out_fname}")
