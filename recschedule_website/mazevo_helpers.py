import os
from datetime import datetime
from typing import List, Tuple

import requests

from recschedule_website.utils import CustomDate, Schedule

# This is for MIT Open Rec
endpoint = "https://east.mymazevo.com/api/PublicCalendar/GetEvents"


def mazevo_api_key():
    return os.environ.get("MAZEVO_API_KEY")


def get_mazevo_bookings(
    start_time: datetime, end_time: datetime
) -> Tuple[List[dict], dict]:
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
        "apiKey": mazevo_api_key(),
    }
    response = requests.post(endpoint, json=payload)
    response = response.json()
    bookings = response["bookings"]

    # also return payload for debugging purposes, remove API key though
    payload.pop("apiKey")
    return bookings, payload


def is_shared_session(booking: dict) -> bool:
    event_name = booking["eventName"].strip()
    # Event name must exactly match "Open Rec" for shared sessions
    if event_name != "Open Rec":
        return False

    building_desc = booking["buildingDescription"]
    room_desc = booking["roomDescription"]

    # Filter valid badminton rooms inside the buildings
    if building_desc == "du Pont (W31/32)":
        return room_desc in {"Du Pont Court 1", "Du Pont Court 2"}
    elif building_desc == "Rockwell (W33)":
        return room_desc in {"North Court", "South Court"}
    else:
        return False


def shorten_building_name(building: str) -> str:
    if building == "du Pont (W31/32)":
        return "du Pont"
    elif building == "Rockwell (W33)":
        return "Rockwell"
    else:
        return building


def shorten_room_name(room: str) -> str:
    if room.startswith("Du Pont"):
        return room.split("Du Pont ")[1]
    else:
        return room


def get_badminton_schedules(
    bookings: List[dict], include_shared_sessions: bool
) -> List[Schedule]:
    schedules = []
    for booking in bookings:
        if booking["timeZone"] != "Eastern Standard Time":
            raise ValueError(
                f"Timezone is not Eastern Standard Time: {booking['timeZone']}"
            )

        # Skip booking if it's not a badminton session and shared sessions are excluded
        is_badminton = "badminton" in booking["eventName"].lower()
        if not is_badminton and not include_shared_sessions:
            continue

        # If it's not badminton but shared sessions are included, check if it's shared
        is_shared = (
            not is_badminton and include_shared_sessions and is_shared_session(booking)
        )
        if not is_badminton and not is_shared:
            continue

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
            building=shorten_building_name(booking["buildingDescription"]),
            room=shorten_room_name(booking["roomDescription"]),
            shared=is_shared,
        )
        schedules.append(schedule)

    return schedules
