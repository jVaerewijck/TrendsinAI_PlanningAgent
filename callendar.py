from ics import Calendar, Event
from datetime import datetime, timedelta
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

def is_overlapping(event1, event2):
    return event1.begin < event2.end and event1.end > event2.begin

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
    if ":" in geplande_uren:  # Format is HH:MM
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
        event = Event()
        event.name = f"Meeting with {klantnaam}"
        event.begin = datetime.combine(event_day, start_time)
        event.duration = timedelta(hours=duration_hours)
        event.description = f"Scheduled hours: {duration_hours}"
        event.location = "Location not specified"

        conflict_found = False
        for existing_event in calendar.events:
            if is_overlapping(event, existing_event):
                conflict_found = True
                print(f"Conflict detected: {event.name} overlaps with {existing_event.name}")
        
        if not conflict_found:
            calendar.events.add(event)
            print(f"Event added to calendar")

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