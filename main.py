from datetime import datetime, timedelta
import ollama
import csv
import os

import callendar
import inputdata

if __name__ == "__main__":
    print("Welcome to the AI calendar planner!\nLet me know when you want to schedule an appointment.")
    appointment_request = input()
    
    # ----- originele code:

    modelfile = """
    FROM llama3.2:latest
    PARAMETER temperature 0.5
    """

    ollama.create(model='calender_ollama', modelfile=modelfile)

    response = ollama.generate(model='calender_ollama', prompt=appointment_request)

    # ----- (after 19/01/2025 modelfile error): replace by:
    # Update these lines:
    modelfile = """
    FROM llama3.2:latest
    PARAMETER temperature 0.5
    """
    # pull the base model
    #ollama.pull('llama2.3')

    # Then create your custom model
    response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'system',
            'content': 'You are a helpful calendar planning assistant'
        },
        {
            'role': 'user',
            'content': appointment_request
        }
    ])

    
    print(response['response'])
    appointment_data = inputdata.parse_appointment_request(appointment_request)

    print(f"Following data will be used for your appointment:\n {appointment_data}")

    inputdata.write_to_database(appointment_data)

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