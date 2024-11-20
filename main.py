from datetime import datetime, timedelta
import csv
import os

import callendar

if __name__ == "__main__":
    filename = "my_calendar.ics"
    database = "db.csv"
    calendar = callendar.create_or_load_calendar(filename)
    start_date = datetime(2024, 11, 18)

    with open(database, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            klantnaam = row['klantnaam']
            geplande_uren = row['geplande_uren']
            tijdsvoorkeur = row['tijdsvoorkeur']
            dag = row['dag']
            frequentie = row['frequentie']

            callendar.add_event_to_calendar(calendar, klantnaam, geplande_uren, tijdsvoorkeur, dag, frequentie, start_date)

    with open(filename, 'w') as file:
        file.writelines(calendar)
    print(f"Events added to {filename}")