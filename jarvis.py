import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install SpeechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Greeting function
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you")

# Listen to the user's command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except:
            print("Timeout reached. Try speaking again.")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Could not recognize speech. Try again.")
        return "None"
    return query

# Send email function
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')  # Replace these
        server.sendmail('youremail@gmail.com', to, content)
        server.quit()
    except Exception as e:
        print(f"Email failed: {e}")
        raise

# Main program
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if query == "none":
            continue

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak("Sorry, I couldn't find information on that topic.")

        elif 'open youtube and search for' in query:
            search_term = query.replace("open youtube and search for", "").strip()
            search_url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
            speak(f"Searching YouTube for {search_term}")
            webbrowser.open(search_url)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com/")
            speak("Opening YouTube")

        elif 'punjabi music' in query:
            speak("Playing Punjabi music on YouTube.")
            webbrowser.open("https://www.youtube.com/watch?v=Iq575foPNpk&list=RDIq575foPNpk&start_radio=1")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif 'open stackoverflow' in query:
            webbrowser.open("https://stackoverflow.com")
            speak("Opening Stack Overflow")

        elif 'linkedin' in query:
            webbrowser.open("https://pk.linkedin.com/")
            speak("Opening LinkedIn")

        elif 'open canva' in query:
            webbrowser.open("https://www.canva.com/")
            speak("Opening Canva")

        elif 'play music' in query:
            song_path = r"D:\Feelinga Garry Sandhu - HDYaar.Com.mp4"  # Replace with actual path
            if os.path.exists(song_path):
                speak("Playing music now.")
                os.startfile(song_path)
            else:
                speak("Sorry, I can't find that music file.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            if os.path.exists(codePath):
                os.startfile(codePath)
                speak("Opening Visual Studio Code")
            else:
                speak("VS Code path not found.")

        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "harryyourEmail@gmail.com"  # Replace with real email
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend Harry bhai, I am not able to send this email")

        elif 'quit' in query or 'exit' in query:
            speak("Okay sir, shutting down. Have a nice day!")
            break
