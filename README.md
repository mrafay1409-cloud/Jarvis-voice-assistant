# Jarvis-voice-assistant
Python voice assistant that listens, speaks, searches Wikipedia and opens websites. 
import datetime
import os
import smtplib
import webbrowser

import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install SpeechRecognition pyaudio
import wikipedia  # pip install wikipedia

# ---------------- Settings (change these for your own computer) ----------------
# Put your own music file here, e.g. a "music" folder next to this script.
MUSIC_PATH = os.path.join(os.path.dirname(__file__), "music", "song.mp4")

# Path to VS Code on Windows (works for any user name).
VSCODE_PATH = os.path.join(
    os.path.expanduser("~"),
    "AppData", "Local", "Programs", "Microsoft VS Code", "Code.exe",
)

# Email login is read from environment variables, NOT written in the code.
# Use a Gmail "App Password", not your normal password.
EMAIL = os.getenv("JARVIS_EMAIL")
PASSWORD = os.getenv("JARVIS_APP_PASSWORD")

# People you can email by voice: say "email to <name>"
CONTACTS = {
    "harry": "friend@example.com",  # replace with a real address
}

# Websites you can open by voice: say "open <name>"
WEBSITES = {
    "google": "https://www.google.com",
    "stackoverflow": "https://stackoverflow.com",
    "linkedin": "https://pk.linkedin.com/",
    "canva": "https://www.canva.com/",
}
# -------------------------------------------------------------------------------

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
# Use the second voice if the computer has one, otherwise the first.
engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)


def speak(audio):
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Say that again please...")
    except sr.RequestError as e:
        print(f"Speech service error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return "None"


def send_email(to, content):
    if not EMAIL or not PASSWORD:
        raise ValueError("Set JARVIS_EMAIL and JARVIS_APP_PASSWORD first.")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, to, content)
    server.quit()


def search_wikipedia(query):
    speak("Searching Wikipedia...")
    topic = query.replace("wikipedia", "").strip()
    try:
        results = wikipedia.summary(topic, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("That topic has many meanings. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I could not find that on Wikipedia.")
    except Exception as e:
        print(e)
        speak("Sorry, something went wrong while searching.")


def main():
    wish_me()
    while True:
        query = take_command().lower()

        if query == "none":
            continue

        if "wikipedia" in query:
            search_wikipedia(query)

        elif "open youtube and search for" in query:
            search_term = query.replace("open youtube and search for", "").strip()
            url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
            speak(f"Searching YouTube for {search_term}")
            webbrowser.open(url)

        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com/")

        elif "punjabi music" in query:
            webbrowser.open(
                "https://www.youtube.com/watch?v=Iq575foPNpk&list=RDIq575foPNpk&start_radio=1"
            )

        elif "play music" in query:
            if os.path.exists(MUSIC_PATH):
                speak("Playing music now.")
                os.startfile(MUSIC_PATH)
            else:
                speak("I could not find your music file. Please check MUSIC_PATH.")

        elif "the time" in query:
            time_now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {time_now}")

        elif "open code" in query:
            if os.path.exists(VSCODE_PATH):
                os.startfile(VSCODE_PATH)
            else:
                speak("I could not find VS Code. Please check VSCODE_PATH.")

        elif "email to" in query:
            name = query.replace("email to", "").strip()
            if name not in CONTACTS:
                speak(f"I don't have an email for {name}.")
                continue
            try:
                speak("What should I say?")
                content = take_command()
                send_email(CONTACTS[name], content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email.")

        elif "quit" in query or "exit" in query:
            speak("Okay sir, shutting down. Have a nice day!")
            break

        else:
            # Generic "open <site>" for any site listed in WEBSITES
            for name, url in WEBSITES.items():
                if f"open {name}" in query or name in query:
                    speak(f"Opening {name}")
                    webbrowser.open(url)
                    break


if __name__ == "__main__":
    main()
