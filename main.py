from calendar import month
from time import monotonic
import pyttsx3
import speech_recognition as sr
import pywhatkit as kit
import datetime
import subprocess
import wikipedia
import requests
import webbrowser
import os
import smtplib
import config

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Jarvis Sir. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        query = query.replace(" a ", " ")

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("www.google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   

        elif "send whatsapp message" in query:
            speak('Please enter the mobile number in the console Sir.')
            number = input("Enter mobile number: ")
            speak("What is the message Sir?")
            message = takeCommand().lower()
            kit.sendwhatmsg_instantly(f"+91{number}", message)
            # kit.sendwhatmsg(f"+91{number}", message, int(datetime.datetime.now().hour), int(datetime.datetime.now().minute) + 2)
            speak("The message has been sent.")

        elif 'weather' in query:
            # query.replace(" now", "")
            lis = list(query.split(" "))
            city = lis[len(lis) - 1]

            res = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.weather_api_key}&units=metric").json()
            weather = res["weather"][0]["main"]
            temperature = res["main"]["temp"]
            feels_like = res["main"]["feels_like"]

            speak(f"The current temperature in {city} is {temperature}℃, but it feels like {feels_like}℃")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature} ℃\nFeels like: {feels_like} ℃")

        elif 'note' in query:
            # takes note and exits
            speak('What do I note Sir?')
            text = takeCommand()
            while(text == 'None'):
                speak("Please say it again Sir")
                text = takeCommand()

            date = datetime.datetime.now()
            file_name = str(date).replace(":", "-") + "-note.txt"
            with open(file_name, "w") as f:
                f.write(text)
            notepad = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\notepad.exe"
            subprocess.Popen([notepad, file_name])

        elif 'play music' in query:
            music_dir = 'C:\\Users\\HP\\Music'
            songs = os.listdir(music_dir)
            # print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Time: {strTime}")
            speak(f"Sir, the time is {strTime}")

        elif 'date' in query:
            day = datetime.datetime.now().day
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year

            dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

            print(f"Date: {day}-{month}-{year}")
            speak(f"Sir, today's date is {day} {dict[month]} {year}")

        elif 'open code' in query:
            codePath = "C:\\Users\\HP\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk"
            os.startfile(codePath)

        elif 'exit' in query or 'sleep' in query:
            speak("Have a good day Nishant!! Until next time.....")
            exit()  


        elif 'none' in query:
            speak("Pardon! I didn't hear you.")

        else:
            speak("Sorry! I am not trained to do that") 