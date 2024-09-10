from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

import datefinder
import pytz

BOSTON_TZ = pytz.timezone("America/New_York")

BUILDING_TO_ADDRESS = {
    "du Pont": "du Pont Athletic Gymnasium, Massachusetts Ave, Cambridge, MA 02139, USA",
    "Rockwell": "Rockwell Cage, 120 Vassar St, Cambridge, MA 02139, USA",
}


@dataclass(frozen=True)
class CustomDate:
    """
    Date without year, month and day only.
    Needed as we use both string and datetime representation.
    """

    date_str: str

    @property
    def datetime(self) -> datetime:
        datetimes = list(datefinder.find_dates(self.date_str))
        assert len(datetimes) == 1
        return datetimes[0]

    def __str__(self):
        return self.date_str


@dataclass(frozen=True)
class Schedule:
    date: CustomDate
    start_time: str
    end_time: str
    building: str
    room: str

    # Whether the session is shared with other sports
    shared: bool = False

    tooltip_button: ClassVar[str] = '<button class="shared-tooltip">?</button>'

    def __post_init__(self):
        if self.building not in BUILDING_TO_ADDRESS:
            raise ValueError(f"Building {self.building} not recognized")

    @property
    def location(self):
        return f"{self.building} {self.room}"

    def to_html(self) -> str:
        shared_html = (
            f" &ndash; Shared Session {self.tooltip_button}" if self.shared else ""
        )
        return (
            f"{self.start_time} - {self.end_time}, {self.location} {shared_html}"
            f'<span>[<a href="{self.create_google_calendar_link()}">Google Cal</a>]</span>'
        )

    def hh_mm_to_utc_str(self, hh_mm_str: str) -> str:
        # Input format = \d{1,2}:\d{2} AM|PM
        # Parse the hour and minutes from the string
        hour = int(hh_mm_str.split(":")[0])
        minutes = int(hh_mm_str.split(":")[1].split(" ")[0])
        am_or_pm = hh_mm_str.split(":")[1].split(" ")[1]

        if am_or_pm == "PM" and hour != 12:
            hour += 12

        # Convert to local timezone and then UTC for Google Calendar
        date = self.date.datetime
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
        if self.shared:
            # Add note if session is shared
            url += "%0ANote: this is a shared session with other sports!"
        url += f"&location={BUILDING_TO_ADDRESS.get(self.building, self.building)}"
        url += f"&dates={self.start_time_utc_str}%2F{self.end_time_utc_str}"
        return url.replace(" ", "%20")
