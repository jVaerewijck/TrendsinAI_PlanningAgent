from ics import Calendar, Event
from datetime import datetime, timedelta, time, timezone
import os
import csv

DAG_TO_INDEX = {
    "maandag": 0,
    "dinsdag": 1,
    "woensdag": 2,
    "donderdag": 3,
    "vrijdag": 4,
    "zaterdag": 5, 
    "zondag": 6,
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

def is_overlapping(calendar,start_time,duration_hours,event_days,klantnaam):
    for event_day in event_days:
        event_start = datetime.combine(event_day, start_time, tzinfo=timezone.utc)
        event_end = event_start + timedelta(hours=duration_hours)
        for existing_event in calendar.events:
            if event_start < existing_event.end and event_end > existing_event.begin:
                print(f"Conflict detected: Meeting with {klantnaam} overlaps with {existing_event.name}")
                return True
    return False

def create_or_load_calendar(filename='my_calendar.ics'):
    calendar = Calendar()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            calendar = Calendar(file.read())
    return calendar

def add_event_to_calendar(calendar, klantnaam, geplande_uren, tijdsvoorkeur, dag, frequency, start_date):
    dag_index = DAG_TO_INDEX.get(dag.lower())
    if dag_index is None:
        print(f"Unknown day: {dag}")
        return
    duration_hours = 0
    start_time = datetime.strptime(tijdsvoorkeur, "%H:%M").time()
    if ":" in geplande_uren:
        hours, minutes = map(int, geplande_uren.split(":"))
        duration_hours = hours + minutes / 60
    else:
        duration_hours = float(geplande_uren)

    event_days = []
    if frequency == '1':
        event_days = [start_date + timedelta(days=dag_index), start_date + timedelta(days=7 + dag_index)]
    elif frequency == '2':
        event_days = [start_date + timedelta(days=7 + dag_index)]

    for event_day in event_days:
        while True:
            conflict_found = False
            if is_overlapping(calendar,start_time,duration_hours,event_days,klantnaam):
                conflict_found = True
                print("Please give a different starting time and/or day")
                print("New day:")
                new_day = input()
                if not new_day == '':
                    dag_index = DAG_TO_INDEX.get(new_day.lower())
                    if frequency == '1':
                        event_day = start_date + timedelta(days=dag_index)
                        event_days[1] = start_date + timedelta(days=7 + dag_index)
                    if frequency == '2':
                        event_day = start_date + timedelta(days=7 + dag_index)
                print("New time:")
                new_time = input()
                if not new_time == '':
                    if ":" in new_time:
                        hours, minutes = map(int, new_time.split(":"))
                    else:
                        hours = int(float(new_time))
                        minutes = int((float(new_time) - hours) * 60)
                    start_time = time(hour=hours, minute=minutes)
            
            event = Event()
            event.name = f"Meeting with {klantnaam}"
            event.begin = datetime.combine(event_day, start_time)
            event.duration = timedelta(hours=duration_hours)
            event.description = f"Scheduled hours: {duration_hours}"
            event.location = "Location not specified"
            
            if not conflict_found:
                calendar.events.add(event)
                print(f"Event added to calendar")
                break

if __name__ == "__main__":
    filename = "my_calendar.ics"
    database = "db.csv"
    calendar = create_or_load_calendar(filename)
    start_date = datetime(2024, 11, 18)

    with open(database, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            klantnaam = row['klantnaam']
            geplande_uren = row['geplande_uren']
            tijdsvoorkeur = row['tijdsvoorkeur']
            dag = row['dag']
            frequentie = row['frequentie']

            add_event_to_calendar(calendar, klantnaam, geplande_uren, tijdsvoorkeur, dag, frequentie, start_date)

    with open(filename, 'w') as file:
        file.writelines(calendar)
    print(f"Events added to {filename}")