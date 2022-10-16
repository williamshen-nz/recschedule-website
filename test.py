from recschedule_website.parser import compare
from recschedule_website.types import CustomDate, Schedule

print(
    compare(
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="7:00 AM",
            end_time="8:00 AM",
            location="Rockwell SOUTH CT",
        )
    )
    < compare(
        Schedule(
            date=CustomDate(date_str="Saturday, March 5, 2022"),
            start_time="7:00 AM",
            end_time="10:00 AM",
            location="du Pont DU PONT CT1",
        )
    )
)
