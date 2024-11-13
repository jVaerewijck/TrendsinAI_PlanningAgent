import ollama
import os
import csv
import json

print("Welcome to the AI calendar planner!\nLet me know when you want to schedule an appointment.")
appointment_request = input()
#appointment_request = "I want to schedule an appointment on thursday 14h every 2 weeks, it will take 4h. My name is Jarno."

modelfile = """
FROM llama3.2:latest
PARAMETER temperature 0.5
"""

ollama.create(model='calender_ollama', modelfile=modelfile)

response = ollama.generate(model='calender_ollama', prompt=appointment_request)

print(response['response'])

def parse_appointment_request(request):
    # Use Ollama to extract appointment details
    prompt = f"Extract the following information from this appointment request: day, time, duration, name, and frequency. Format as JSON. don't show extra text, i want only the json as a response. Request: {request}"
    response = ollama.generate(model='calender_ollama', prompt=prompt)
    
    # Convert the response string to a Python dictionary
    json_response = json.loads(response['response'])
    return json_response

# Get the structured data
appointment_data = parse_appointment_request(appointment_request)

# Write to CSV database
def write_to_database(appointment_data):
    if not os.path.exists('db.csv'):
        with open('db.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'start_time', 'duration', 'name'])
    
    with open('db.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            appointment_data['day'],
            appointment_data['time'],
            appointment_data['duration'],
            appointment_data['name']
        ])

# Call the function with the parsed data
write_to_database(appointment_data)