from datetime import datetime
from typing import NamedTuple

import datefinder
import pytz

BOSTON_TZ = pytz.timezone("America/New_York")

LOCATION_TO_ADDRESS = {
    "du Pont DU PONT CT1": "du Pont Athletic Gymnasium, Massachusetts Ave, Cambridge, MA 02139, USA",
    "du Pont DU PONT CT2": "du Pont Athletic Gymnasium, Massachusetts Ave, Cambridge, MA 02139, USA",
    "Rockwell NORTH CT": "Rockwell Cage, 120 Vassar St, Cambridge, MA 02139, USA",
    "Rockwell SOUTH CT": "Rockwell Cage, 120 Vassar St, Cambridge, MA 02139, USA",
}


class Schedule(NamedTuple):
    date: str
    start_time: str
    end_time: str
    location: str

    def to_html(self):
        return (
            self.start_time
            + " - "
            + self.end_time
            + ", "
            + self.location
            + f' [<a href="{self.create_google_calendar_link()}">Google Cal</a>]'
        )

    def hh_mm_to_utc_str(self, hh_mm_str: str) -> str:
        # Input format = \d{1,2}:\d{2} AM|PM
        # Extract date from string
        date = list(datefinder.find_dates(self.date))
        assert len(date) == 1
        date = date[0]

        # Parse the hour and minutes from the string
        hour = int(hh_mm_str.split(":")[0])
        minutes = int(hh_mm_str.split(":")[1].split(" ")[0])
        am_or_pm = hh_mm_str.split(":")[1].split(" ")[1]

        if am_or_pm == "PM" and hour != 12:
            hour += 12

        # Convert to local timezone and then UTC for Google Calendar
        start_date = datetime(date.year, date.month, date.day, hour, minutes)
        local_datetime = BOSTON_TZ.localize(start_date, is_dst=None)

        # e.g. 20220223T193300Z
        utc_datetime = local_datetime.astimezone(pytz.utc)
        return utc_datetime.strftime("%Y%m%dT%H%M%SZ")

    @property
    def start_time_utc_str(self):
        return self.hh_mm_to_utc_str(self.start_time)

    @property
    def end_time_utc_str(self):
        return self.hh_mm_to_utc_str(self.end_time)

    def create_google_calendar_link(self) -> str:
        url = "https://www.google.com/calendar/render?action=TEMPLATE"
        url += f"&text=Badminton ({self.location})"
        url += (
            f"&details=MIT Badminton Open Recreation%0ASession: {self.start_time} "
            f"to {self.end_time}%0ALocation: {self.location}"
        )
        url += f"&location={LOCATION_TO_ADDRESS.get(self.location, self.location)}"
        url += f"&dates={self.start_time_utc_str}%2F{self.end_time_utc_str}"
        return url.replace(" ", "%20")
