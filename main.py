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
    
    start_time = datetime.strptime(tijdsvoorkeur, "%H:%M").time()
    duration_hours = float(geplande_uren)

    event_days = []
    if frequency == '1':
        event_days = [start_date + timedelta(days=dag_index), start_date + timedelta(days=7 + dag_index)]
    elif frequency == '2':
        event_days = [start_date + timedelta(days=7 + dag_index)]

    for event_day in event_days:
        event = Event()
        event.name = "Meeting with {klantnaam}"
        event.begin = datetime.combine(event_day, start_time)
        event.duration = timedelta(hours=duration_hours)
        event.description = f"Scheduled hours: {geplande_uren}"
        event.location = "Location not specified"

        calendar.events.add(event)

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
            dag = int(row['dag'])
            frequency = row['frequentie']

            add_event_to_calendar(calendar, klantnaam, geplande_uren, tijdsvoorkeur, dag, frequency, start_date)

    with open(filename, 'w') as file:
        file.writelines(calendar)
    print(f"Event added to {filename}")