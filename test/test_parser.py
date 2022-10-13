from recschedule_website.parser import extract_dates, get_schedules_for_dates
from recschedule_website.types import CustomDate, Schedule


def test_extract_dates(recschedule_txt: str):
    dates = extract_dates(recschedule_txt)
    print(dates)
    assert dates == [
        CustomDate(date_str="Thursday, March 3, 2022"),
        CustomDate(date_str="Friday, March 4, 2022"),
        CustomDate(date_str="Friday, March 4, 2022"),
        CustomDate(date_str="Saturday, March 5, 2022"),
        CustomDate(date_str="Saturday, March 5, 2022"),
        CustomDate(date_str="Sunday, March 6, 2022"),
        CustomDate(date_str="Sunday, March 6, 2022"),
        CustomDate(date_str="Monday, March 7, 2022"),
        CustomDate(date_str="Monday, March 7, 2022"),
        CustomDate(date_str="Tuesday, March 8, 2022"),
        CustomDate(date_str="Tuesday, March 8, 2022"),
        CustomDate(date_str="Wednesday, March 9, 2022"),
        CustomDate(date_str="Wednesday, March 9, 2022"),
        CustomDate(date_str="Thursday, March 10, 2022"),
        CustomDate(date_str="Friday, March 11, 2022"),
        CustomDate(date_str="Saturday, March 12, 2022"),
        CustomDate(date_str="Saturday, March 12, 2022"),
        CustomDate(date_str="Sunday, March 13, 2022"),
    ]


def test_get_schedule_for_dates(recschedule_txt: str):
    custom_dates = extract_dates(recschedule_txt)
    date_to_schedules = get_schedules_for_dates(custom_dates, recschedule_txt)

    assert date_to_schedules == {
        CustomDate(date_str="Thursday, March 3, 2022"): [
            Schedule(
                date=CustomDate(date_str="Thursday, March 3, 2022"),
                start_time="6:00 AM",
                end_time="4:00 PM",
                location="du Pont DU PONT CT1",
            ),
            Schedule(
                date=CustomDate(date_str="Thursday, March 3, 2022"),
                start_time="6:00 AM",
                end_time="10:30 AM",
                location="Rockwell NORTH CT",
            ),
        ],
        CustomDate(date_str="Friday, March 4, 2022"): [
            Schedule(
                date=CustomDate(date_str="Friday, March 4, 2022"),
                start_time="6:00 AM",
                end_time="5:00 PM",
                location="du Pont DU PONT CT1",
            ),
            Schedule(
                date=CustomDate(date_str="Friday, March 4, 2022"),
                start_time="6:00 AM",
                end_time="3:00 PM",
                location="Rockwell NORTH CT",
            ),
        ],
        CustomDate(date_str="Saturday, March 5, 2022"): [
            Schedule(
                date=CustomDate(date_str="Saturday, March 5, 2022"),
                start_time="7:00 AM",
                end_time="10:00 AM",
                location="du Pont DU PONT CT1",
            ),
            Schedule(
                date=CustomDate(date_str="Saturday, March 5, 2022"),
                start_time="7:00 AM",
                end_time="8:00 AM",
                location="Rockwell SOUTH CT",
            ),
            Schedule(
                date=CustomDate(date_str="Saturday, March 5, 2022"),
                start_time="1:30 PM",
                end_time="2:30 PM",
                location="du Pont DU PONT CT1",
            ),
            Schedule(
                date=CustomDate(date_str="Saturday, March 5, 2022"),
                start_time="4:00 PM",
                end_time="9:00 PM",
                location="Rockwell SOUTH CT",
            ),
            Schedule(
                date=CustomDate(date_str="Saturday, March 5, 2022"),
                start_time="5:30 PM",
                end_time="9:00 PM",
                location="du Pont DU PONT CT1",
            ),
        ],
        CustomDate(date_str="Sunday, March 6, 2022"): [
            Schedule(
                date=CustomDate(date_str="Sunday, March 6, 2022"),
                start_time="9:00 AM",
                end_time="11:00 PM",
                location="du Pont DU PONT CT1",
            ),
            Schedule(
                date=CustomDate(date_str="Sunday, March 6, 2022"),
                start_time="6:00 PM",
                end_time="11:00 PM",
                location="Rockwell NORTH CT",
            ),
        ],
        CustomDate(date_str="Monday, March 7, 2022"): [
            Schedule(
                date=CustomDate(date_str="Monday, March 7, 2022"),
                start_time="6:00 AM",
                end_time="4:00 PM",
                location="du Pont DU PONT CT1",
            ),
            Schedule(
                date=CustomDate(date_str="Monday, March 7, 2022"),
                start_time="6:00 AM",
                end_time="10:30 AM",
                location="Rockwell SOUTH CT",
            ),
        ],
        CustomDate(date_str="Tuesday, March 8, 2022"): [
            Schedule(
                date=CustomDate(date_str="Tuesday, March 8, 2022"),
                start_time="6:00 AM",
                end_time="3:00 PM",
                location="du Pont DU PONT CT1",
            ),
            Schedule(
                date=CustomDate(date_str="Tuesday, March 8, 2022"),
                start_time="12:30 PM",
                end_time="3:15 PM",
                location="Rockwell SOUTH CT",
            ),
        ],
        CustomDate(date_str="Wednesday, March 9, 2022"): [
            Schedule(
                date=CustomDate(date_str="Wednesday, March 9, 2022"),
                start_time="6:00 AM",
                end_time="4:30 PM",
                location="du Pont DU PONT CT1",
            ),
            Schedule(
                date=CustomDate(date_str="Wednesday, March 9, 2022"),
                start_time="6:00 AM",
                end_time="10:30 AM",
                location="Rockwell SOUTH CT",
            ),
        ],
        CustomDate(date_str="Thursday, March 10, 2022"): [
            Schedule(
                date=CustomDate(date_str="Thursday, March 10, 2022"),
                start_time="6:00 AM",
                end_time="3:30 PM",
                location="du Pont DU PONT CT1",
            ),
            Schedule(
                date=CustomDate(date_str="Thursday, March 10, 2022"),
                start_time="12:15 PM",
                end_time="4:45 PM",
                location="Rockwell SOUTH CT",
            ),
            Schedule(
                date=CustomDate(date_str="Thursday, March 10, 2022"),
                start_time="10:00 PM",
                end_time="11:00 PM",
                location="Rockwell SOUTH CT",
            ),
        ],
        CustomDate(date_str="Friday, March 11, 2022"): [],
        CustomDate(date_str="Saturday, March 12, 2022"): [],
        CustomDate(date_str="Sunday, March 13, 2022"): [
            Schedule(
                date=CustomDate(date_str="Sunday, March 13, 2022"),
                start_time="9:00 AM",
                end_time="12:00 PM",
                location="du Pont DU PONT CT1",
            )
        ],
    }


def test_get_schedule_for_dates_include_open_rec(recschedule_txt: str):
    custom_dates = extract_dates(recschedule_txt)
    date_to_schedules = get_schedules_for_dates(custom_dates, recschedule_txt, include_shared_open_rec=True)
    assert date_to_schedules[CustomDate(date_str="Thursday, March 3, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Thursday, March 3, 2022"),
            start_time="6:00 AM",
            end_time="10:30 AM",
            location="Rockwell NORTH CT",
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 3, 2022"),
            start_time="6:00 AM",
            end_time="10:30 AM",
            location="Rockwell SOUTH CT",
            shared=True
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 3, 2022"),
            start_time="6:00 AM",
            end_time="4:00 PM",
            location="du Pont DU PONT CT1",
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 3, 2022"),
            start_time="6:00 AM",
            end_time="4:00 PM",
            location="du Pont DU PONT CT2",
            shared=True
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 3, 2022"),
            start_time="7:30 PM",
            end_time="11:00 PM",
            location="du Pont DU PONT CT1",
            shared=True
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 3, 2022"),
            start_time="10:00 PM",
            end_time="11:00 PM",
            location="du Pont DU PONT CT2",
            shared=True
        ),
    ]

    assert date_to_schedules[CustomDate(date_str="Friday, March 4, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Friday, March 4, 2022"),
            start_time="6:00 AM",
            end_time="3:00 PM",
            location="Rockwell NORTH CT",
        ),
        Schedule(
            date=CustomDate(date_str="Friday, March 4, 2022"),
            start_time="6:00 AM",
            end_time="5:00 PM",
            location="du Pont DU PONT CT1",
        ),
    ]

    assert date_to_schedules[CustomDate(date_str="Saturday, March 5, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="7:00 AM",
            end_time="8:00 AM",
            location="Rockwell SOUTH CT",
        ),
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="7:00 AM",
            end_time="10:00 AM",
            location="du Pont DU PONT CT1",
        ),
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="7:00 AM",
            end_time="10:00 AM",
            location="du Pont DU PONT CT2",
            shared=True
        ),
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="1:30 PM",
            end_time="2:30 PM",
            location="du Pont DU PONT CT1",
        ),
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="3:00 PM",
            end_time="9:00 PM",
            location="du Pont DU PONT CT2",
            shared=True
        ),
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="4:00 PM",
            end_time="9:00 PM",
            location="Rockwell SOUTH CT",
        ),
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="5:30 PM",
            end_time="9:00 PM",
            location="du Pont DU PONT CT1",
        ),
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="6:00 PM",
            end_time="9:00 PM",
            location="Rockwell NORTH CT",
            shared=True
        ),
    ]

    assert date_to_schedules[CustomDate(date_str="Sunday, March 6, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Sunday, March 6, 2022"),
            start_time="9:00 AM",
            end_time="11:00 PM",
            location="du Pont DU PONT CT1",
        ),
        Schedule(
            date=CustomDate(date_str="Sunday, March 6, 2022"),
            start_time="6:00 PM",
            end_time="11:00 PM",
            location="Rockwell NORTH CT",
        ),
    ]

    assert date_to_schedules[CustomDate(date_str="Monday, March 7, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Monday, March 7, 2022"),
            start_time="6:00 AM",
            end_time="10:30 AM",
            location="Rockwell SOUTH CT",
        ),
        Schedule(
            date=CustomDate(date_str="Monday, March 7, 2022"),
            start_time="6:00 AM",
            end_time="4:00 PM",
            location="du Pont DU PONT CT1",
        ),
    ]

    assert date_to_schedules[CustomDate(date_str="Tuesday, March 8, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Tuesday, March 8, 2022"),
            start_time="6:00 AM",
            end_time="10:30 AM",
            location="Rockwell NORTH CT",
            shared=True
        ),
        Schedule(
            date=CustomDate(date_str="Tuesday, March 8, 2022"),
            start_time="6:00 AM",
            end_time="3:00 PM",
            location="du Pont DU PONT CT1",
        ),
        Schedule(
            date=CustomDate(date_str="Tuesday, March 8, 2022"),
            start_time="12:30 PM",
            end_time="3:15 PM",
            location="Rockwell SOUTH CT",
        ),
        Schedule(
            date=CustomDate(date_str="Tuesday, March 8, 2022"),
            start_time="7:30 PM",
            end_time="11:00 PM",
            location="du Pont DU PONT CT1",
            shared=True
        ),
    ]

    assert date_to_schedules[CustomDate(date_str="Wednesday, March 9, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Wednesday, March 9, 2022"),
            start_time="6:00 AM",
            end_time="10:30 AM",
            location="Rockwell SOUTH CT",
        ),
        Schedule(
            date=CustomDate(date_str="Wednesday, March 9, 2022"),
            start_time="6:00 AM",
            end_time="4:30 PM",
            location="du Pont DU PONT CT1",
        ),
        Schedule(
            date=CustomDate(date_str="Wednesday, March 9, 2022"),
            start_time="10:00 PM",
            end_time="11:00 PM",
            location="du Pont DU PONT CT2",
            shared=True
        ),
    ]
    assert date_to_schedules[CustomDate(date_str="Thursday, March 10, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Thursday, March 10, 2022"),
            start_time="6:00 AM",
            end_time="3:30 PM",
            location="du Pont DU PONT CT1",
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 10, 2022"),
            start_time="12:15 PM",
            end_time="4:45 PM",
            location="Rockwell SOUTH CT",
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 10, 2022"),
            start_time="7:00 PM",
            end_time="9:00 PM",
            location="du Pont DU PONT CT1",
            shared=True
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 10, 2022"),
            start_time="7:00 PM",
            end_time="9:00 PM",
            location="du Pont DU PONT CT2",
            shared=True
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 10, 2022"),
            start_time="10:00 PM",
            end_time="11:00 PM",
            location="Rockwell SOUTH CT",
        ),
        Schedule(
            date=CustomDate(date_str="Thursday, March 10, 2022"),
            start_time="10:00 PM",
            end_time="11:00 PM",
            location="du Pont DU PONT CT2",
            shared=True
        ),
    ]
    assert date_to_schedules[CustomDate(date_str="Friday, March 11, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Friday, March 11, 2022"),
            start_time="6:00 AM",
            end_time="9:30 AM",
            location="Rockwell SOUTH CT",
            shared=True
        ),
    ]
    assert date_to_schedules[CustomDate(date_str="Saturday, March 12, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Saturday, March 12, 2022"),
            start_time="5:00 PM",
            end_time="8:00 PM",
            location="du Pont DU PONT CT1",
            shared=True
        ),
    ]

    assert date_to_schedules[CustomDate(date_str="Sunday, March 13, 2022")] == [
        Schedule(
            date=CustomDate(date_str="Sunday, March 13, 2022"),
            start_time="9:00 AM",
            end_time="10:30 AM",
            location="du Pont DU PONT CT2",
            shared=True
        ),
        Schedule(
            date=CustomDate(date_str="Sunday, March 13, 2022"),
            start_time="9:00 AM",
            end_time="12:00 PM",
            location="du Pont DU PONT CT1",
        )
    ]
