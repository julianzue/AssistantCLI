import os
import gtts
from playsound import playsound
import speech_recognition as sr
import time
import random
from uptime import uptime
from datetime import datetime, timedelta
import wikipedia

from colorama import Fore, init

init()

r = Fore.LIGHTRED_EX
y = Fore.LIGHTYELLOW_EX
g = Fore.LIGHTGREEN_EX
c = Fore.LIGHTCYAN_EX

R = Fore.RESET

count = 0

def speak(sentence):

    t = "[" + time.strftime("%H:%M:%S") + "] "

    if sentence == "Listening...":
        print(t + y + sentence + R)

    elif sentence == "Could not understand.":
        print(t + r + sentence + R)

    elif sentence.startswith("You said"):
        print(t + r + sentence + R)

    elif sentence == "I have no action with this command.":
        print(t + r + sentence + R)

    elif sentence == "Please try again.":
        print(t + r + sentence + R)

    elif sentence == "Sorry there was an error.":
        print(t + r + sentence + R)

    else:
        print(t + g + sentence + R)

    tts = gtts.gTTS(sentence)
    tts.save("speak.mp3")
    playsound("speak.mp3")

def randomJoke():
    randValue = random.randint(0, 3)

    if randValue == 0:
        speak("Did you hear about the mathematician who’s afraid of negative numbers?")
        speak("He’ll stop at nothing to avoid them.")
    
    elif randValue == 1:
        speak("What do you call a boomerang that won’t come back?")
        speak("A stick.")

    elif randValue == 2:
        speak("What falls in winter but never gets hurt?")
        speak("Snow.")

    elif randValue == 3:
        speak("Can a kangaroo jump higher than a house?")
        speak("Of course! Houses can't jump.")

def stand_by():
    re = sr.Recognizer()

    print("[" + time.strftime("%H:%M:%S") + "] "+ y + "Say 'turn on' to end stand by mode." + R)

    with sr.Microphone() as source2:
        re.adjust_for_ambient_noise(source=source2, duration=1)
        audio2 = re.listen(source2)

        try:
            if re.recognize_google(audio2) == "turn on":
                speak("Stand by mode deactivated!")
                print("")
                recognize()
        except sr.UnknownValueError:
            pass

    stand_by()

def recognize():
    global count

    r = sr.Recognizer()

    with sr.Microphone() as source:
        if count == 0:
            os.system("clear")

            print(c + "Speech Recognition".upper() + R)
            print(c + "==================" + R)
            print("")
            speak("Welcome to speech recognition!")
            print("")

            count += 1

        r.adjust_for_ambient_noise(source=source, duration=1)
        speak("Listening...")
        audio = r.listen(source)

        try:
            #print("[" + time.strftime("%H:%M:%S") + "] " + c + str(r.recognize_google(audio)) + R)

            if r.recognize_google(audio) == "good morning":
                speak("Good Morning. How can I help you?")

            elif r.recognize_google(audio) == "open Google Chrome":
                speak("Opening Google Chrome...")
                os.system("xfce4-terminal -e 'google-chrome' &")

            elif r.recognize_google(audio) == "open YouTube":
                speak("Opening YouTube on Google Chrome...")
                os.system("xfce4-terminal -e 'google-chrome https://www.youtube.com' &")

            elif r.recognize_google(audio) == "open Facebook":
                speak("Opening Facebook on Google Chrome...")
                os.system("xfce4-terminal -e 'google-chrome https://www.facebook.com' &")

            elif r.recognize_google(audio) == "open calendar":
                speak("Opening Calendar...")
                os.system("gnome-calendar &")

            elif r.recognize_google(audio) == "open File Explorer":
                speak("Opening File Explorer...")
                os.system("thunar /home/julian/ &")

            elif r.recognize_google(audio) == "open media player":
                speak("Opening VLC Media Player...")
                os.system("xfce4-terminal -e vlc &")

            elif r.recognize_google(audio) == "play music":
                speak("Playing music on VLC Media Player...")

                paths = [
                    "/home/julian/Videos/Results/ManOnTheMoon.mp4",
                    "/home/julian/Videos/Results/Habit.mp4"
                ]

                randValue = random.randint(0, (len(paths) - 1))

                os.system("xfce4-terminal -e 'vlc " + paths[randValue] + "' &")

            elif r.recognize_google(audio) == "what's the time":
                speak("It is " + time.strftime("%H:%M") + " now.")

            elif r.recognize_google(audio) == "which day is today":

                if time.strftime("%d") == "1":
                    number = "st"
                elif time.strftime("%d") == "2":
                    number = "nd"
                else:
                    number = "th"

                speak("It is " + time.strftime("%A the %d" + number +" %B, %Y"))

            elif r.recognize_google(audio).startswith("search"):
                speak("Starting google search about '" + r.recognize_google(audio)[7:] + "' on Google Chrome...")
                os.system("xfce4-terminal -e 'google-chrome https://www.google.com/search?q=" + str(r.recognize_google(audio)[7:]).replace(" ", "+") + "' &")

            elif r.recognize_google(audio) == "open calculator":
                speak("Opening Calculator")
                os.system("gnome-calculator &")

            elif r.recognize_google(audio) == "open email":
                speak("Opening Mozilla Thunderbird...")
                os.system("thunderbird &")

            elif r.recognize_google(audio) == "time":
                res = datetime.fromtimestamp(uptime()) - timedelta(hours=1)

                speak("Your Computers uptime is:")
                speak(str(res.time())[:8])

            elif r.recognize_google(audio) == "tell me a joke":
                randomJoke()

            elif r.recognize_google(audio).startswith("what is"):
                try:
                    speak(str(wikipedia.summary(r.recognize_google(audio)[8:], sentences=1)))
                except wikipedia.exceptions.DisambiguationError or wikipedia.exceptions.PageError or wikipedia.exceptions.WikipediaException:
                    speak("Sorry there was an error.")

            elif r.recognize_google(audio).startswith("calculate"):
                split = str(r.recognize_google(audio)).split(" ")

                value1 = split[1]
                operator = split[2]
                value2 = split[3]

                if operator == "+" or operator == "plus":
                    result = int(value1) + int(value2)
                    speak(value1 + " + " + value2 + " = " + str(result))

                elif operator == "*" or operator == "times" or operator == "x":
                    result = int(value1) * int(value2)
                    speak(value1 + " * " + value2 + " = " + str(result))

                elif operator == "-" or operator == "minus":
                    result = int(value1) - int(value2)
                    speak(value1 + " - " + value2 + " = " + str(result))

                elif operator == "/" or operator == "devided":
                    result = int(value1) / int(value2)
                    speak(value1 + " / " + value2 + " = " + str(result))

            elif r.recognize_google(audio) == "stand by":
                speak("Switch to stand by mode!")
                print("")
                stand_by()

            elif r.recognize_google(audio) == "help" or r.recognize_google(audio) == "what can I say":
                speak("This are your possibilities:")
                speak("good morning")
                speak("open Google Chrome")
                speak("open YouTube")
                speak("open Facebook")
                speak("open Calendar")
                speak("open File Explorer")
                speak("open Calculator")
                speak("open Email")
                speak("open Media Player")
                speak("tell me a joke")
                speak("play music")
                speak("what's the time")
                speak("which day is today")
                speak("search ...")
                speak("help")
                speak("time")
                speak("calculate ...")
                speak("what can I say")
                speak("what is ...")
                speak("exit")

            elif r.recognize_google(audio) == "exit":
                speak("Exiting program.")
                quit()

            else:
                speak("You said: '" + r.recognize_google(audio) + "'.")
                speak("I have no action with this command.")
                
        except sr.UnknownValueError:
            speak("Could not understand.")
            speak("Please try again.")

        except sr.RequestError as e:
            print(r + "Error: " + "{0}".format(e) + R)

    print("")
    recognize()

recognize()