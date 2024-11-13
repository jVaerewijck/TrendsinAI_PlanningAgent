from ics import Calendar, Event
from datetime import datetime, timedelta
import os

filename = 'my_calendar.ics'
calendar = Calendar()
if os.path.exists(filename):
    with open(filename, 'r') as file:
        calendar = Calendar(file.read())

event_title = 'Meeting with Team'
start_time = datetime(2023, 11, 13, 10, 0)  # e.g., November 13, 2023, at 10:00 AM
duration = 2  # in hours
description = 'Discuss project updates'
location = 'Office Room 2'

event = Event()
event.name = event_title
event.begin = start_time
event.duration = timedelta(hours=duration)
event.description = description
event.location = location

calendar.events.add(event)

with open(filename, 'w') as file:
    file.writelines(calendar)

print(f"Event added to {filename}")