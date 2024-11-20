import ollama
import os
import csv
import json

FREQUENCY_TO_INDEX = {
    "every week": 1,
    "every 2 weeks": 2
    }



def parse_appointment_request(request):
    # Use Ollama to extract appointment details
    prompt = f"Extract the following information from this appointment request: day, time (in hh:mm format), duration (in hh:mm format), name, and frequency. Format as JSON. don't show extra text, i want only the json as a response and a personal reply message like 'event scheduled' and no questions. Request: {request}"
    response = ollama.generate(model='calender_ollama', prompt=prompt)
    
    # Convert the response string to a Python dictionary
    json_response = json.loads(response['response'])
    return json_response


def validate_appointment_data(appointment_data):
    required_fields = ['name', 'duration', 'time', 'day', 'frequency']
    missing_fields = []
    
    for field in required_fields:
        if field not in appointment_data or not appointment_data[field]:
            missing_fields.append(field)
    
    return missing_fields

def get_missing_field_input(field):
    return input(f"Please enter the {field} for your appointment: ")

# Write to CSV database
def write_to_database(appointment_data):

    missing_fields = validate_appointment_data(appointment_data)

    while missing_fields:
        print(f"Missing information for: {', '.join(missing_fields)}")
        
        # Get missing fields from user
        for field in missing_fields:
            appointment_data[field] = get_missing_field_input(field)
        
        # Revalidate
        missing_fields = validate_appointment_data(appointment_data)


    if not os.path.exists('db.csv'):
        with open('db.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['klantnaam','geplande_uren','tijdsvoorkeur','dag','frequentie'])
    
    #frequency doorsturen
    frequency_index = FREQUENCY_TO_INDEX.get(appointment_data['frequency'].lower())
    if frequency_index is None:
        print(f"Invalid frequency. Please use one of: {', '.join(FREQUENCY_TO_INDEX.keys())}")
        return

    try:
        with open('test_db.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                appointment_data['name'],
                appointment_data['duration'],
                appointment_data['time'],
                appointment_data['day'],
                frequency_index
            ])
            print("Data written to CSV successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
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
    # Get the structured data
    appointment_data = parse_appointment_request(appointment_request)

    print(f"Following data will be used for your appointment:\n {appointment_data}")

    # Call the function with the parsed data
    write_to_database(appointment_data)


#main.py to check if it overlaps and AI can answer and request the user to make a new appointment