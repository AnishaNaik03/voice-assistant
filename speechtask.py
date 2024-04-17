import datetime
import wikipedia
import pywhatkit
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
import pyttsx3

engine = pyttsx3.init()

# Download NLTK data (you only need to do this once)
#nltk.download('punkt')

prev_intent = None

def talk(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        talk("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)  # Listen for 5 seconds
            #talk("Transcribing...")
            print("Transcribing...")
            text = recognizer.recognize_google(audio, language="en-US")
            return text.lower()
        except sr.WaitTimeoutError:
            talk("Sorry, I couldn't hear anything.")
            return ""
        except sr.UnknownValueError:
            talk("Sorry, I couldn't understand what you said.")
            return ""

def analyze_command(command):
    global prev_intent

    # Tokenize the command
    tokens = word_tokenize(command)

    if 'play' in tokens:
        index = tokens.index('play')
        song = ' '.join(tokens[index+1:])
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)
        prev_intent = "play_music"
    elif 'time' in tokens:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {current_time}")
        prev_intent = "get_time"
    elif 'date' in tokens:
        current_date = datetime.datetime.now().strftime('%d %B %Y')
        talk(f"Today's date is {current_date}")
        prev_intent = "get_date"
    elif any(word in tokens for word in ['how', 'are', 'you']):
        talk("I'm doing well, thank you.")
        prev_intent = "greet"
    elif all(word in tokens for word in ['your', 'name']):
        talk("My name is Jarvis. What's yours?")
        prev_intent = "ask_name"
    elif all(word in tokens for word in ['exit']) or any(word in tokens for word in ['goodbye']):
        talk("Goodbye!")
        exit()
    elif all(word in tokens for word in ['who', 'is']):
        try:
            person_index = tokens.index('is') + 1
            person = ' '.join(tokens[person_index:])
            info = wikipedia.summary(person, sentences=1)
            talk(info)
            prev_intent = "lookup_person"
        except wikipedia.exceptions.DisambiguationError:
            talk("Please be clear.")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find information about that.")
    else:
        # Handle unknown commands or maintain context
        if prev_intent == "lookup_person":
            # If previous intent was to lookup a person, try again
            talk("Sorry, I couldn't find information about that person. Please try again.")
        elif prev_intent == "ask_name":
            # If previous intent was to ask for name, respond with a greeting
            talk("Nice to meet you!")
        else:
            talk("I'm not sure what you're asking. Please repeat.")

def run_jarvis():
    while True:
        command = transcribe_speech()
        if command:
            print("User:", command)
            analyze_command(command)

if __name__ == "__main__":
    run_jarvis()
