import speech_recognition as sr
import random
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
from google_trans_new import google_translator 
from win10toast import ToastNotifier
import pywhatkit
import playsound
import threading
from gtts import gTTS 

# Importing Essential Modules above

speaker = 'internal' # Variable for selecting engine(internal or google)
toast = ToastNotifier() # Creating Notifier object
manual_path = "data\manual_addition.json" # Path of the manually added conversation/responses
backup_path = r"data\backup\backup.json" # Backup path of the manually added responses

with open(manual_path) as f: # Reading the manual responses and saving in variable manual_addition
  manual_addition = json.load(f)

print('Loading your AI personal assistant')

current = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0' #Key of current voice

engine=pyttsx3.init('sapi5') # Initilising pyttsx3

voices=engine.getProperty('voices') # getting details of available voices

engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0') #setting the current voice as ZIRA
available_voices = [voice.id for voice in voices] # List containing keys of available voices

def google_speak(mytext, language = 'en'): # Function to speak using gtts for different languages
    myobj = gTTS(text=mytext, lang=language, slow=False) #Creating gtts Object
    myobj.save("temporary.mp3") # Saving the said text as mp3
    playsound.playsound("temporary.mp3", block=True) # playing above mp3 using playsound module
    os.system("del temporary.mp3") # deleting the generated mp3

def speak(text):
    global speaker # Checking which engine to use
    if speaker == 'internal': 
        engine.say(text) # Using the interna engine to speak
        engine.runAndWait()
    else:
        google_speak(text) # Using gtts to speak
def wishMe():
    hour=datetime.datetime.now().hour # getting the current hour and greeting accordingly
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")

def voice_input(): # Function to take voice input
    r=sr.Recognizer() #Creating the recognizer object
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source) # Listening and saving the data in audio

        try:
            statement=r.recognize_google(audio,language='en') # Recognising the audio and generating the text
            print(f"user said:{statement}\n") # Printing the text

        except Exception as e: # In case the recognition fails, execute this part
            speak("Pardon me, please say that again")
            return "None"
        return statement

def change_voice():
    global current
    if available_voices.index(current) + 1 >len(available_voices) - 1: # Checking if it is the last voice in list
        assistant_voice = 0
    else:
        assistant_voice = available_voices.index(current) + 1
    current = available_voices[assistant_voice]
    print(current)
    engine.setProperty('voice',f'{current}') # changing voice

def translate(text, to):
    lang_codes = {"hindi": "hi-in", "english":"en-us", "japanese":"ja-jp", "german": "de-de", "korean": "ko-kr", "greek": "el-gr"}
    # dictionary containing codes of the languages, more can be added
    if to.lower() in lang_codes:
        to = lang_codes[to.lower()]
    translator = google_translator() # Initialising google translate
    translate_text = translator.translate(text,lang_tgt=to) # Generating translated text
    google_speak(translate_text, to.split('-')[0]) # Using gtts to speak the different language
    print(translate_text)


def solve():
    speak('I can answer to computational and geographical questions,,, what question do you want to ask now')
    question=voice_input()
    app_id="R2K75H-7ELALHR35X"
    client = wolframalpha.Client('R2K75H-7ELALHR35X') # Initialising WolfRam Alpha
    res = client.query(question) # Sending query to WolfRam Alpha
    answer = next(res.results).text # Receiving the answer as text
    print(answer)
    speak(answer)

def help(): # Function to get help, can be improved further
    speak("Want to see a list of tasks that you can get help on?")
    query = voice_input()
    if query == "yes":
        speak("You can say one of the following to get commands and help")
        usage_list = ["how to use wikipedia",
                    "how to open youtube",
                    "how to open gmail",
                    "how to open google",
                    "how to check weather",
                    "how to check news",
                    "how to ask math questions",
                    "how to change voice",
                    "how to open stackoverflow",
                    "how to search on google",
                    "how to take picture",
                    "how to log out",
                    "how to ask time",
                    "how to quit"]
        for i in usage_list:
            print(i)
            speak(i)
    query = voice_input().lower()
    description = [
    """
    To use wikipedia, say:

    wikipedia and then the topic name
    such as

    wikipedia diffraction

    Try to be more specific as vague questions can cause error
    """,
    """
    To open youtube, say:

    open youtube
    """,
    """
    To open gmail, say:

    open gmail
    """,
    """
    To open google, say:

    open youtube
    """,
    """
    To check weather, say: weather and I will ask you the city name.
    """,
    """
    To check news, say:

    news
    """,
    """
    to ask math questions, say : ask then I will ask you the questions
    """,
    """
    To change voice, say:

    change voice
    """,
    """
    To open stackoverflow, say:

    open stackoverflow
    """,
    """
    To search on web, say: search and then the query,

    such as,

    search the highest mountain peak
    """,

    """
    To take a photo, say:

    take a photo,, or, camera
    """,
    """
    To log out, say:

    log out
    """,
    """
    To ask the time, say:

    time
    """,
    """
    To quit, say:

    good bye, or, bye, or , stop
    """
    ]

    try:
        speak(description[usage_list.index(query)])
        print(description[usage_list.index(query)])
    except:
        speak("oops, some error occured")

def sleep(minutes):
    speak(f"See you in {minutes} minutes") # Using time.sleep() to make the assistant stop for given minutes
    time.sleep(60*minutes)

def notify(title, text, duration):
    toast.show_toast(title, text, duration = duration) # Using the Notifier object to show custom Notifications, ONly works in Windows 10

def add_response(): # Creating function to add responses
    """
    We are using a dictionary to store the user query as key and response as value
    if a value is there then we can replace/add/remove.
    """
    global manual_addition, manual_path
    speak("Please enter the query you want to add response to")
    query = voice_input().lower()
    if query=="none":
        speak("I could not hear that")
    if query not in manual_addition:
        speak("Speak the response that you want me to give.")
        response = voice_input().lower()
        while response=="none":
            speak("Speak the response that you want me to give.")
            response = voice_input().lower()
        manual_addition[query] = [response]
    else:
        speak("A response is already there, do you want to replace or add another")
        choice = voice_input().lower()
        while choice=="none":
                speak("Speak the response that you want me to give.")
                choice = voice_input().lower()
        if choice == "replace":
            speak("Speak the new response that you want me to give.")
            response = voice_input().lower()
            while response=="none":
                speak("Speak the response that you want me to give.")
                response = voice_input().lower()
            manual_addition[query] = [response]
        elif choice == "add another":
            speak("Speak the additional random response you want me to give")
            response = voice_input().lower()
            while response=="none":
                speak("Speak the response that you want me to give.")
                response = voice_input().lower()
            manual_addition[query] += [response]
        else:
            speak("Some error occured")
    with open(manual_path, "w") as outfile:
        json.dump(manual_addition, outfile)

def remove_response():
    """
    Made this function using the same concept as add_response but instead to reove the response only
    """
    global manual_addition, manual_path
    speak("which response you wan to remove")
    query = voice_input().lower()
    if query in manual_addition:
        if len(manual_addition[query]) == 1:
            del manual_addition[query]
        else:
            speak("Multiple responses found, do you want to say the response or listen to all first")
            choose = voice_input().lower()
            while choose=="none":
                speak("Speak the response that you want me to give.")
                choose = voice_input().lower()
            if choose == "say the response":
                speak("Please say thre response you want to delete")
                response = voice_input().lower()
                while response=="none":
                    speak("Speak the response that you want me to give.")
                    response = voice_input().lower()
                if response in manual_addition[query]:
                    speak("No such response found")
                else:
                    manual_addition[query].remove(key)
            else:
                for i, j in enumerate(manual_addition[query]):
                    speak(f"{i+1}. {j}")
        with open(manual_path, "w") as outfile:
            json.dump(manual_addition, outfile)
    else:
        speak("No such manual response exist")
def reset_response():
    """
    Deletes the manual addition file (Backup can be created)
    """
    global manual_addition
    speak("Are you sure you want to delete all saved responses?")
    choose = voice_input()
    if choose == "yes":
        speak("Do you want to save backup?")
        choice = voice_input()
        if choice == "no":
            manual_addition = {}
            with open(manual_path, "w") as outfile:
                json.dump(manual_addition, outfile)
        else:
            speak("A backup file will be created")
            with open(backup_path, "w") as outfile:
                json.dump(manual_addition, outfile)
            manual_addition = {}
            with open(manual_path, "w") as outfile:
                json.dump(manual_addition, outfile)
        speak("Restart the application for changes to take effect")

    else:
        speak("No response was deleted")
        return
def load_backup():
    """
    If a backup of manual addition is created before reset then you can load using this
    """
    global manual_addition
    with open(backup_path) as f:
        manual_addition = json.load(f)
    with open(manual_path, "w") as outfile:
        json.dump(manual_addition, outfile)
    speak("Restart the application for changes to take effect")

def switch_talker(): # changin the speaker variable to change the engine
    global speaker
    if speaker == 'internal':
        speaker = 'google'
    else:
        speaker = 'internal'

def timer(minutes, description): # Using threadin module to delay the notify function by given minutes
    freq = threading.Timer(60*minutes, notify, args = ["Personal Assistant", description, 3])
    freq.start()
    
speak("Loading your AI personal assistant")
