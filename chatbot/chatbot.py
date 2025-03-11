import tkinter as tk
from tkinter import scrolledtext, filedialog
import pyttsx3
import speech_recognition as sr
import os
import json

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Voice Assistant Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Voice Input Function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            chat_display.insert(tk.END, "Listening...\n")
            audio = recognizer.listen(source)
            user_query = recognizer.recognize_google(audio)
            return user_query
        except sr.UnknownValueError:
            return "I didn't catch that. Please try again."

# Global variable to store responses loaded from a file
loaded_responses = {}

def load_responses(file_path):
    """
    Load responses from a JSON file where questions and answers are structured as:
    {
        "questions_and_answers": [
            {"You": "question", "Chatbot": "response"},
            ...
        ]
    }
    """
    global loaded_responses
    loaded_responses = {}  # Reset responses
    if not os.path.exists(file_path):
        chat_display.insert(tk.END, f"Error: File '{file_path}' not found.\n")
        return
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            for qa in data.get("questions_and_answers", []):
                question = qa.get("You", "").lower()  # Extract question
                answer = qa.get("Chatbot", "")  # Extract answer
                if question and answer:
                    loaded_responses[question] = answer  # Store in dictionary
        chat_display.insert(tk.END, f"Responses loaded successfully from file '{file_path}'.\n")
    except Exception as e:
        chat_display.insert(tk.END, f"Error reading file: {e}\n")

def chatbot_response(query):
    """
    Generate chatbot response based on query.
    Priority: Loaded file responses > Predefined responses > Default response
    """
    query = query.lower()  # Convert query to lowercase for case-insensitive matching

    # Check loaded responses first
    response = loaded_responses.get(query, None)
    if response:
        return response

    # If no match in loaded responses, check predefined responses
    predefined_responses = {
        "hello": "Hi there! How can I assist you?",
        "how are you": "I'm just a chatbot, but I'm here to help!",
        "what is ai": "AI stands for Artificial Intelligence, enabling machines to mimic human intelligence.",
        "bye": "Goodbye! Have a nice day!",
    }

    return predefined_responses.get(query, "I'm sorry, I didn't quite understand that. Please try rephrasing.")

# GUI Functions
def send_message():
    """
    Handle sending message from the input box.
    """
    user_input = entry.get()
    if user_input:
        chat_display.insert(tk.END, f"You: {user_input}\n", "user_message")
        entry.delete(0, tk.END)
        response = chatbot_response(user_input)
        chat_display.insert(tk.END, f"Chatbot: {response}\n", "chatbot_message")
        chat_display.yview(tk.END)
        speak(response)

def handle_enter(event):
    send_message()

def start_voice_chat():
    """
    Handle voice input and response.
    """
    user_query = listen()
    chat_display.insert(tk.END, f"You (via Voice): {user_query}\n", "user_message")
    response = chatbot_response(user_query)
    chat_display.insert(tk.END, f"Chatbot: {response}\n", "chatbot_message")
    chat_display.yview(tk.END)
    speak(response)

def select_file():
    """
    Open file dialog to select a response file and load responses.
    """
    file_path = filedialog.askopenfilename(title="Select Response File", filetypes=(("JSON files", ".json"), ("All files", ".")))
    if file_path:
        load_responses(file_path)

# GUI Setup
window = tk.Tk()
window.title("MINI CHATBOT")
window.geometry("1000x800")
window.configure(bg='#2e2e2e')

# Chat Display
chat_display = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=25, bg="#333333", fg="#f0f0f0", font=("Arial", 12))
chat_display.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Add custom tags for message colors
chat_display.tag_configure("user_message", foreground="#00bfff", font=("Arial", 12, "bold"))
chat_display.tag_configure("chatbot_message", foreground="#32cd32", font=("Arial", 12))

# Input Box
entry = tk.Entry(window, width=50, font=("Arial", 18), bd=2, relief="solid")
entry.grid(row=1, column=0, padx=10, pady=10)

# Buttons
send_button = tk.Button(window, text="Send", width=12, font=("Arial", 12), bg="#4CAF50", fg="white", activebackground="#45a049", command=send_message)
send_button.grid(row=1, column=1, padx=5, pady=10)

voice_button = tk.Button(window, text="🎙 Voice", width=12, font=("Arial", 12), bg="#FF5722", fg="white", activebackground="#e64a19", command=start_voice_chat)
voice_button.grid(row=2, column=1, padx=5, pady=10)

file_button = tk.Button(window, text="Load File", width=12, font=("Arial", 12), bg="#2196F3", fg="white", activebackground="#0b7dda", command=select_file)
file_button.grid(row=2, column=0, padx=5, pady=10)

# Bind Enter Key to Send Message
window.bind('<Return>', handle_enter)

# Welcome Message
chat_display.insert(tk.END, "Chatbot: Welcome! Type your question or use the voice button to speak.\n", "chatbot_message")

# Load responses from the 'abc.json' file when the program starts
load_responses('abc.json')

# Run the Application
window.mainloop()
