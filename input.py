import ollama
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