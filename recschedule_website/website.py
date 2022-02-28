from datetime import datetime
from typing import Dict, List

import pytz

from recschedule_website.schedule import Schedule, BOSTON_TZ

HTML_HEAD = """
<html>
<head>
<title>MIT Open Rec Badminton Schedule</title>
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
<p><strong>Notes:</strong> this schedule is updated every 30 minutes from the latest rec schedule 
(<a href="http://web.mit.edu/athletics/www/recschedule.pdf">http://web.mit.edu/athletics/www/recschedule.pdf</a>)</p>
<p>There is no guarantee for accuracy. Please contact willshen at mit.edu with any questions or issues.</p>
<p><a href="https://github.com/williamshen-nz/recschedule-website">Open Source on GitHub</a>. Feel free to contribute!</p>
</body>
</html>
"""


def write_html_for_schedule(
    date_to_schedules: Dict[str, List[Schedule]], fname: str
) -> None:
    current_datetime_in_boston_tz = (
        datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(BOSTON_TZ)
    )

    # Markdown Section
    html_lines = [
        HTML_HEAD,
        "<h2>MIT Open Rec Badminton - Unofficial Schedule</h2>",
        f"<p>Last updated on {current_datetime_in_boston_tz.strftime('%a, %d %b %Y %-I:%M:%S %p')} Boston time.</p>",
        "<hr>",
    ]

    for date, schedules in date_to_schedules.items():
        html_lines.append(f"<p class='date'><strong>{date}</strong></p>")
        for schedule in schedules:
            html_lines.append("<p>" + schedule.to_html() + "</p>")

    html_lines.append(HTML_END)
    open(fname, "w").write("\n".join(html_lines))
