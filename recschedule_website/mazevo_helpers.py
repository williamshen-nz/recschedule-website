from datetime import datetime
from typing import List, Tuple

import requests

from recschedule_website.utils import CustomDate, Schedule

# This is for MIT Open Rec
endpoint = "https://east.mymazevo.com/api/PublicCalendar/GetEvents"
api_key = "bcf3ed86c61861024ef5d7bcf30389d7"


def get_mazevo_bookings(start_time: datetime, end_time: datetime) -> Tuple[List[dict], dict]:
    """Call Mazevo API to get bookings between start_time and end_time"""
    if start_time >= end_time:
        raise ValueError("Start time must be before end time")

    payload = {
        "start": start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "end": end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "buildingIds": None,
        "roomTags": ["OPEN REC "],
        "eventTypeIds": [87],
        "statusIds": [1],
        "organizationIds": None,
        "organizationTypeIds": None,
        "hideSpecialDates": False,
        "userOffsetMinutes": 240,
        "apiKey": api_key,
    }
    response = requests.post(endpoint, json=payload)
    response = response.json()
    bookings = response["bookings"]
    # also return payload for debugging purposes
    return bookings, payload


def get_badminton_schedules(
    bookings: List[dict], include_shared_sessions: bool = False
) -> List[Schedule]:
    if include_shared_sessions:
        raise NotImplementedError(f"Shared sessions not implemented yet")

    badminton_bookings = filter(
        lambda booking: "badminton" in booking["eventName"].lower(), bookings
    )
    schedules = []

    for booking in badminton_bookings:
        if booking["timeZone"] != "Eastern Standard Time":
            raise ValueError(
                f"Timezone is not Eastern Standard Time: {booking['timeZone']}"
            )
        # Format: YYYY-MM-DDTHH:MM:SS-04:00
        start_time = booking["dateTimeStart"]
        end_time = booking["dateTimeEnd"]

        # Strip the timezone and parse
        assert start_time.endswith("-04:00")
        assert end_time.endswith("-04:00")
        start_time = datetime.strptime(start_time[:-6], "%Y-%m-%dT%H:%M:%S")
        end_time = datetime.strptime(end_time[:-6], "%Y-%m-%dT%H:%M:%S")
        assert start_time.date() == end_time.date()

        # Turn date into friendly format, e.g. Monday, February 23
        date_str = start_time.date().strftime("%A, %B %d")
        custom_date = CustomDate(date_str)

        schedule = Schedule(
            date=custom_date,
            start_time=start_time.strftime("%-I:%M %p"),
            end_time=end_time.strftime("%-I:%M %p"),
            location=f"{booking['buildingDescription']} {booking['roomDescription']}",
            shared=False,
        )
        schedules.append(schedule)

    return schedules
