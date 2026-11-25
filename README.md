# Jarvis-voice-assistant
Python voice assistant that listens, speaks, searches Wikipedia and opens websites. 
# Jarvis - Python Voice Assistant

A voice-controlled desktop assistant built with Python. It listens to your commands and replies with speech.

## Features
- Speaks and listens using voice commands
- Searches Wikipedia and YouTube
- Opens websites and apps (Google, LinkedIn, Canva, VS Code)
- Tells the current time
- Plays music from a local file
- Sends emails by voice

## Tech Used
Python, pyttsx3, SpeechRecognition, wikipedia, smtplib

## Setup
1. Install the libraries:
   pip install pyttsx3 SpeechRecognition wikipedia pyaudio
2. Set your email details as environment variables (use a Gmail App Password):
   JARVIS_EMAIL and JARVIS_APP_PASSWORD
3. Run the assistant:
   python jarvis.py

## Example Commands
- "Wikipedia Python programming"
- "Open YouTube and search for lo-fi music"
- "What is the time"
- "Open Google"
- "Exit"

## Future Plans
- Add AI answers using an LLM API
- Add weather and to-do list features
