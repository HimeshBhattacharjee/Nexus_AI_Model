import pyttsx3
import pyautogui
import time
import datetime
import socket
import pyjokes
import requests
import speech_recognition as sr
import wikipedia
import webbrowser
import keyboard
import os
import smtplib
import ssl
import re
import openai
import serial
import subprocess
from apikey import api_data
import pywhatkit as kit
from bs4 import BeautifulSoup
from requests import get
from datetime import date
from PIL import ImageGrab
from AppOpener import close
import winsdk.windows.devices.geolocation as wdg, asyncio

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 175)
engine.setProperty('volume', 50.0)


openai.api_key = api_data
completion = openai.Completion()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():

    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("\nGood Morning!", end=" ")
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        print("\nGood Afternoon!", end=" ")
        speak("Good Afternoon!")

    else:
        print("\nGood Evening!", end=" ")
        speak("Good Evening!")

    print("I am Nexus.")
    speak("I am Nexus.")
    today = date.today()
    today = datetime.datetime.now().strftime("%d %B, %Y")
    print("Sir, today's date is", today, end=" ")
    speak("Sir, today's date is" + today)
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"and the time is {time}")
    speak(f"and the time is {time}")
    print("Please tell me how may I help you?")
    speak("Please tell me how may I help you?")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 9000
        r.dynamic_energy_threshold = False
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, snowboy_configuration=None,
                        phrase_time_limit=5)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "NONE"
    return query


def sendEmail(content):
    context = ssl.create_default_context()
    emails = ["rabitraatashankar.2003@gmail.com","mamoarpita.2003@gmail.com","datachunks2k23@gmail.com"]
    for dest in emails:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls(context=context)
        server.login('omandabamema.2130@gmail.com', 'yupqjyozdjlizpwf')
        server.sendmail("omandabamema.2130@gmail.com", dest, content)
        server.quit()


def play_on_youtube(video):
    kit.playonyt(video)


def Temperature():
    city = query.split("in", 1)
    soup = BeautifulSoup(requests.get(
        f"https://www.google.com/search?q=weather+in+{city[0]}").text, "html.parser")
    region = soup.find("span", class_="BNeawe tAd8D AP7Wnd")
    temp = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
    day = soup.find("div", class_="BNeawe tAd8D AP7Wnd")
    weather = day.text.split("m", 1)
    temperature = temp.text.split("c", 1)
    print("Its Currently"+weather[1]+" and "+temperature[0]+" in "+region.text)
    speak("Its Currently"+weather[1]+" and "+temperature[0]+" in "+region.text)


def Reply(question):
    prompt = f'Himesh: {question}\n Nexus: '
    response = completion.create(
        prompt=prompt, engine="text-davinci-003", stop=['\Himesh'], max_tokens=2000)
    answer = response.choices[0].text.strip()
    return answer


def Gesture():
    ArduinoSerial = serial.Serial('COM5', 9600)
    time.sleep(2)
    c = 0
    while 1:
        c += 1
        incoming = str(ArduinoSerial.readline())
        print(incoming)

        if 'Rewind' in incoming:
            pyautogui.press('right')

        if 'Forward' in incoming:
            pyautogui.press('left')

        if 'Volume Up' in incoming:
            pyautogui.press('up')

        if 'Volume Down' in incoming:
            pyautogui.press('down')

        if 'Play/Pause' in incoming:
            pyautogui.typewrite(['space'], 0.2)

        incoming = ""
        if (c == 30):
            print("Gesture Control Mode over!! Maximum limit reached")
            speak("Gesture Control Mode over!! Maximum limit reached")
            speak("Closing media player")
            close('VLC')
            break
    
async def getCoords():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return pos.coordinate.latitude, pos.coordinate.longitude

def Location():
    print(asyncio.run(getCoords()))
    return asyncio.run(getCoords())


if __name__ == "__main__":
    wishme()
    i = 0
    print("Say 'Nexus' To Wake Me Up")
    while (i < 1):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.energy_threshold = 9000
            r.dynamic_energy_threshold = False
            r.adjust_for_ambient_noise(source)
            audio = r.listen(
                source, snowboy_configuration=None, phrase_time_limit=5)
        try:
            command = r.recognize_google(audio, language="en-in")
            message = command.lower()

            if message == "nexus":
                k = 0
                while k == 0:
                    query = takecommand().lower()

                    if 'sleep' in query or 'hibernate' in query:
                        speak("Entering Sleep Mode. Say Nexus To Wake Me Up!")
                        k = 1
                        print("Say 'Nexus' To Wake Me Up")
                    elif 'nexus answer me' in query or 'answer me' in query:
                        speak("What do you want to know, Sir?")
                        print("What do you want to know, Sir?")
                        query = takecommand().lower()
                        ans = Reply(query)
                        print(ans)
                        speak(ans)
                    elif 'wikipedia' in query:
                        speak("Searching wikipedia")
                        query = query.replace("wikipedia", "")
                        results = wikipedia.summary(query, sentences=2)
                        speak("According to wikipedia")
                        print(results)
                        speak(results)
                    elif 'open google' in query or 'search in google' in query or 'google search' in query or 'launch google' in query:
                        speak('Sir, what do you want to search on Google?')
                        dest = takecommand().lower()
                        if dest == "none":
                            continue
                        url = 'https://www.google.com/search?q='
                        search_url = url+dest
                        webbrowser.open(search_url)
                    elif 'close the tab' in query or 'close google tab' in query or 'close google search' in query or 'close location' in query:
                        keyboard.press_and_release('ctrl+w')
                    elif 'close google' in query:
                        close('chrome',output=False)
                    elif 'open youtube' in query or 'launch youtube' in query:
                        speak('Sir, what do you want to play on Youtube?')
                        video = takecommand().lower()
                        if video == "none":
                            continue
                        play_on_youtube(video)
                    elif 'close the video' in query or 'close youtube' in query or 'close youtube video' in query or 'close video' in query:
                        keyboard.press_and_release('ctrl+w')
                    elif 'play music' in query or 'play spotify' in query or 'play song' in query or 'please song' in query:
                        speak("What song should I say, sir?")
                        song = takecommand().lower()
                        if song == "none":
                            continue
                        os.system('spotify')
                        time.sleep(8)
                        pyautogui.hotkey('ctrl', 'l')
                        time.sleep(1)
                        pyautogui.write(song, interval=0.01)
                        for key in ['enter', 'pagedown', 'tab', 'enter', 'enter']:
                            time.sleep(3)
                            pyautogui.press(key)
                        speak('Playing'+song)
                    elif 'stop music' in query or 'stop the song' in query or 'stop song' in query or 'close spotify' in query or 'close the song' in query:
                        close('spotify',output=False)
                    elif 'what is the weather' in query or 'weather' in query:
                        Temperature()
                    elif 'ip address' in query:
                        hostname = socket.gethostname()
                        IPAddr = socket.gethostbyname(hostname)
                        print("Your Computer Name is " + hostname)
                        print("Your Computer IP Address is " + IPAddr)
                    elif 'joke' in query or 'tell me a joke' in query or 'say a joke' in query:
                        joke = pyjokes.get_joke()
                        print(joke)
                        speak(joke)
                    elif 'take a screenshot' in query or 'get screenshot' in query or 'take screenshot' in query:
                        pic = ImageGrab.grab()
                        pic.show()
                    elif 'close screenshot' in query or 'close ss' in query:
                        subprocess.run(['taskkill', '/f', '/im', 'Microsoft.Photos.exe'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    elif 'send email' in query or 'email' in query or 'write an email' in query:
                        try:
                            speak("What should I say, sir?")
                            content = takecommand()
                            content = re.sub(
                                "full stop", ". ", content, flags=re.IGNORECASE)
                            content = re.sub(
                                "inverted comma open", " ' ", content, flags=re.IGNORECASE)
                            content = re.sub(
                                "inverted open", " ' ", content, flags=re.IGNORECASE)
                            content = re.sub(
                                "inverted comma close", " '", content, flags=re.IGNORECASE)
                            content = re.sub(
                                "inverted close", " '", content, flags=re.IGNORECASE)
                            content = re.sub(
                                "comma", ", ", content, flags=re.IGNORECASE)
                            content = re.sub(
                                "enter", "\n", content, flags=re.IGNORECASE)
                            content = content[0].upper() + content[1:]
                            sendEmail(content)
                            print("Email has been sent!")
                            speak("Email has been sent!")
                        except Exception as e:
                            print(e)
                            speak("Sorry Sir. I am unable to send this email")
                    elif 'what is my current location' in query or 'current location' in query or 'location' in query:
                        s=""
                        for item in Location():
                            s+=str(item)+","
                        s=s[:-1]
                        url = 'https://www.google.com/maps/place/'
                        search_url = url+s
                        webbrowser.open(search_url)
                    elif 'gesture' in query or 'hand control' in query or 'control' in query:
                        os.startfile('C:\\Users\\Himesh\\Videos\\VIdeo\\The.Elephant.Whisperers.2022.1080p.WEBRip.x264.AAC5.1-[YTS.MX].mp4')
                        Gesture()
                    elif 'nexus quit' in query or 'nexus exit' in query or 'nexus close' in query or 'quit' in query:
                        print(
                            "Thanks for using Nexus, Sir. Have a great day ahead!!")
                        speak(
                            "Thanks for using Nexus, Sir. Have a great day ahead!!")
                        exit()
            else:
                continue
        except Exception as e:
            continue
