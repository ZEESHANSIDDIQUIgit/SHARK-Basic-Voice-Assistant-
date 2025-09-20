import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary 
import requests 
import pyjokes  
import pytz
import datetime


# ---------- SPEAK FUNCTION ----------
def speak(text):
    engine = pyttsx3.init()   # create fresh engine every time
    engine.setProperty('rate', 170)   # Adjust speed
    engine.setProperty('volume', 1.0) # Max volume
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    

# -------------for time zone -------------
def get_timezone_from_place(place: str):
    place = place.lower()
    timezones = {
        "pakistan": "Asia/Karachi",
        "india": "Asia/Kolkata",
        "usa": "America/New_York",
        "new york": "America/New_York",
        "los angeles": "America/Los_Angeles",
        "uk": "Europe/London",
        "england": "Europe/London",
        "germany": "Europe/Berlin",
        "china": "Asia/Shanghai",
        "japan": "Asia/Tokyo",
        "dubai": "Asia/Dubai"
    }

    for key in timezones:
        if key in place:
            return timezones[key]

    return None  # agar nahi mila


# ---------- COMMAND PROCESSOR ----------
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        speak("Opening Google 🌐")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c:
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open chat gpt" in c:
        speak("Opening Chat GPT")
        webbrowser.open("https://www.chatgpt.com")
    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("Add your link ")
    elif "open github" in c:
        speak("Opening GitHub")
        webbrowser.open("Add your link ")
    elif "open student portal" in c:
        speak("Opening Student Portal")
        webbrowser.open("Add your link ")
    elif "open playlist" in c:
        speak("Opening Playlist")
        webbrowser.open("Add your link ")
    elif c.startswith("play"):
        song = c.split(" ", 1)[1] if len(c.split(" ")) > 1 else ""
        link = musiclibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "joke" in c:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)
   
    # ✅ Time command
    elif "time" in c:
        speak("Sure, please tell me the city or country 🌍")
        r2 = sr.Recognizer()
        with sr.Microphone() as source:
            r2.adjust_for_ambient_noise(source)
            audio = r2.listen(source, timeout=5, phrase_time_limit=4)
            place = r2.recognize_google(audio)

        tz = get_timezone_from_place(place)
        if tz:
            local_time = datetime.datetime.now(pytz.timezone(tz))
            speak(f"The time in {place} is {local_time.strftime('%I:%M %p')}")
        else:
            speak("Sorry, I could not find the timezone for that location.")

    # ✅ Date command
    elif "date" in c:
        speak("Sure, please tell me the city or country 🌍")
        r2 = sr.Recognizer()
        with sr.Microphone() as source:
            r2.adjust_for_ambient_noise(source)
            audio = r2.listen(source, timeout=5, phrase_time_limit=4)
            place = r2.recognize_google(audio)

        tz = get_timezone_from_place(place)
        if tz:
            local_date = datetime.datetime.now(pytz.timezone(tz))
            speak(f"The date in {place} is {local_date.strftime('%B %d, %Y')}")
        else:
            speak("Sorry, I could not find the timezone for that location.")

    elif "news" in c:
        api_key = "[your api key ]"
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        r = requests.get(url)
        data = r.json()
        titles = [article["title"] for article in data.get("articles", [])]
        
        if titles:
            speak("Here are the latest headlines.")
            for t in titles[:7]:   # read only first 5
                print(t)
                speak(t)
        else:
            speak("Sorry, I couldn't fetch the news.")   

    elif "stop" in c or "exit" in c:
        speak("Goodbye🦈")
        exit()
                   

# ---------- MAIN LOOP ----------
if __name__ == "__main__":
    speak("Spawning 🦈...")

    while True:
        r = sr.Recognizer()
        print("I’m listening 🦈...")

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Waiting for the magic word... try 'Shark' ")
                audio = r.listen(source, timeout=5, phrase_time_limit=4)  
                word = r.recognize_google(audio)

            if word.lower() == "shark":
                speak("Yes 🦈 what can I do for you.")
                print("  SHARK ACTIVATED !!!")

                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    print("Listening for command...")
                    audio = r.listen(source, timeout=7, phrase_time_limit=6)  
                    command = r.recognize_google(audio)
                    print(f"Command received: {command}")

                processCommand(command)

            else:
                print("Wake word not detected. Waiting...")

        except Exception as e:
            print("Recognition error:", e)   
            speak("Sorry, I didn’t catch that. ")
