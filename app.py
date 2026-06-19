from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import webbrowser
import pyjokes
import pytz
import datetime
import requests as req
import os
import re
import random

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


import musiclibrary
music = musiclibrary.music

# ─── Timezone helper ──────────────────────────────────────────────────────────
def get_timezone_from_place(place: str):
    place = place.lower()
    timezones = {
        "pakistan": "Asia/Karachi",
        "karachi": "Asia/Karachi",
        "lahore": "Asia/Karachi",
        "islamabad": "Asia/Karachi",
        "india": "Asia/Kolkata",
        "mumbai": "Asia/Kolkata",
        "delhi": "Asia/Kolkata",
        "usa": "America/New_York",
        "america": "America/New_York",
        "new york": "America/New_York",
        "los angeles": "America/Los_Angeles",
        "chicago": "America/Chicago",
        "uk": "Europe/London",
        "england": "Europe/London",
        "london": "Europe/London",
        "germany": "Europe/Berlin",
        "berlin": "Europe/Berlin",
        "china": "Asia/Shanghai",
        "shanghai": "Asia/Shanghai",
        "japan": "Asia/Tokyo",
        "tokyo": "Asia/Tokyo",
        "dubai": "Asia/Dubai",
        "uae": "Asia/Dubai",
        "australia": "Australia/Sydney",
        "sydney": "Australia/Sydney",
        "melbourne": "Australia/Melbourne",
        "france": "Europe/Paris",
        "paris": "Europe/Paris",
        "canada": "America/Toronto",
        "toronto": "America/Toronto",
        "russia": "Europe/Moscow",
        "moscow": "Europe/Moscow",
        "brazil": "America/Sao_Paulo",
        "south africa": "Africa/Johannesburg",
        "egypt": "Africa/Cairo",
        "cairo": "Africa/Cairo",
        "turkey": "Europe/Istanbul",
        "istanbul": "Europe/Istanbul",
        "saudi arabia": "Asia/Riyadh",
        "riyadh": "Asia/Riyadh",
        "bangladesh": "Asia/Dhaka",
        "dhaka": "Asia/Dhaka",
        "nepal": "Asia/Kathmandu",
        "sri lanka": "Asia/Colombo",
        "thailand": "Asia/Bangkok",
        "bangkok": "Asia/Bangkok",
        "singapore": "Asia/Singapore",
        "malaysia": "Asia/Kuala_Lumpur",
        "kuala lumpur": "Asia/Kuala_Lumpur",
        "philippines": "Asia/Manila",
        "manila": "Asia/Manila",
        "indonesia": "Asia/Jakarta",
        "jakarta": "Asia/Jakarta",
        "south korea": "Asia/Seoul",
        "seoul": "Asia/Seoul",
        "taiwan": "Asia/Taipei",
        "taipei": "Asia/Taipei",
        "hong kong": "Asia/Hong_Kong",
        "mexico": "America/Mexico_City",
        "mexico city": "America/Mexico_City",
        "italy": "Europe/Rome",
        "rome": "Europe/Rome",
        "spain": "Europe/Madrid",
        "madrid": "Europe/Madrid",
        "netherlands": "Europe/Amsterdam",
        "amsterdam": "Europe/Amsterdam",
        "sweden": "Europe/Stockholm",
        "stockholm": "Europe/Stockholm",
        "switzerland": "Europe/Zurich",
        "zurich": "Europe/Zurich",
        "norway": "Europe/Oslo",
        "oslo": "Europe/Oslo",
        "denmark": "Europe/Copenhagen",
        "copenhagen": "Europe/Copenhagen",
        "poland": "Europe/Warsaw",
        "warsaw": "Europe/Warsaw",
        "portugal": "Europe/Lisbon",
        "lisbon": "Europe/Lisbon",
        "ireland": "Europe/Dublin",
        "dublin": "Europe/Dublin",
        "belgium": "Europe/Brussels",
        "brussels": "Europe/Brussels",
        "austria": "Europe/Vienna",
        "vienna": "Europe/Vienna",
        "czech republic": "Europe/Prague",
        "prague": "Europe/Prague",
        "hungary": "Europe/Budapest",
        "budapest": "Europe/Budapest",
        "greece": "Europe/Athens",
        "athens": "Europe/Athens",
        "finland": "Europe/Helsinki",
        "helsinki": "Europe/Helsinki",
        "new zealand": "Pacific/Auckland",
        "auckland": "Pacific/Auckland",
        "argentina": "America/Argentina/Buenos_Aires",
        "buenos aires": "America/Argentina/Buenos_Aires",
        "chile": "America/Santiago",
        "santiago": "America/Santiago",
        "peru": "America/Lima",
        "lima": "America/Lima",
        "colombia": "America/Bogota",
        "bogota": "America/Bogota",
        "venezuela": "America/Caracas",
        "caracas": "America/Caracas",
        "nigeria": "Africa/Lagos",
        "lagos": "Africa/Lagos",
        "kenya": "Africa/Nairobi",
        "nairobi": "Africa/Nairobi",
        "ethiopia": "Africa/Addis_Ababa",
        "addis ababa": "Africa/Addis_Ababa",
        "morocco": "Africa/Casablanca",
        "casablanca": "Africa/Casablanca",
        "israel": "Asia/Jerusalem",
        "jerusalem": "Asia/Jerusalem",
        "iran": "Asia/Tehran",
        "tehran": "Asia/Tehran",
        "iraq": "Asia/Baghdad",
        "baghdad": "Asia/Baghdad",
        "qatar": "Asia/Qatar",
        "doha": "Asia/Qatar",
        "kuwait": "Asia/Kuwait",
        "oman": "Asia/Muscat",
        "muscat": "Asia/Muscat",
        "jordan": "Asia/Amman",
        "amman": "Asia/Amman",
        "lebanon": "Asia/Beirut",
        "beirut": "Asia/Beirut",
    }
    for key in timezones:
        if key in place:
            return timezones[key]
    return None


# ─── Weather helper ───────────────────────────────────────────────────────────
# ✅ LINE 19 (this line): Replace YOUR_OPENWEATHER_API_KEY with your real key
WEATHER_API_KEY = ""

def get_weather(city: str):
    mock = (
        "Weather in {}:\n"
        "Sunny\n"
        "Temp: 28 C\n"
        "Humidity: 65%\n"
        "Wind: 12 km/h\n"
        "(Add your OpenWeather API key in app.py for live data)"
    ).format(city.title())

    if WEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
        return {"response": mock}
    try:
        url = (
            "http://api.openweathermap.org/data/2.5/weather"
            "?q={}&appid={}&units=metric".format(city, WEATHER_API_KEY)
        )
        r = req.get(url, timeout=5)
        data = r.json()
        if data.get("cod") != 200:
            return {"response": "Sorry, I couldn't find weather data for '{}'.".format(city)}
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"].title()
        response_text = (
            "Weather in {}:\n"
            "{}\n"
            "Temp: {} C\n"
            "Humidity: {}%\n"
            "Wind: {} km/h"
        ).format(city.title(), desc, temp, humidity, wind)
        return {"response": response_text}
    except Exception:
        return {"response": mock}


# ─── Greeting helper ──────────────────────────────────────────────────────────
def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"


# ─── Command processor ────────────────────────────────────────────────────────
def process_command(c: str):
    c = c.lower().strip()

    # Greetings
    for g in ["hello", "hi", "hey", "greetings", "what's up", "howdy", "hola"]:
        if g in c:
            return {"response": "{} I'm Shark, your voice assistant. How can I help you today?".format(get_greeting())}

    if "how are you" in c or "how r u" in c:
        return {"response": "I'm swimming smoothly through the digital ocean! Ready to help. What can I do?"}

    if "your name" in c or "who are you" in c:
        return {"response": "I'm Shark Assistant -- your intelligent voice companion. I can open websites, play music, tell jokes, check the time, and much more!"}

    if "thank" in c or "thanks" in c:
        return {"response": "You're welcome! Happy to help anytime. Just say the word!"}

    # Open websites
    site_map = {
        "open google": ("Opening Google", "https://www.google.com"),
        "open youtube": ("Opening YouTube", "https://www.youtube.com"),
        "open facebook": ("Opening Facebook", "https://www.facebook.com"),
        "open chat gpt": ("Opening ChatGPT", "https://www.chatgpt.com"),
        "open chatgpt": ("Opening ChatGPT", "https://www.chatgpt.com"),
        "open linkedin": ("Opening LinkedIn", "https://www.linkedin.com"),
        "open github": ("Opening GitHub", "https://www.github.com"),
        "open twitter": ("Opening Twitter", "https://www.twitter.com"),
        "open x": ("Opening X", "https://www.twitter.com"),
        "open instagram": ("Opening Instagram", "https://www.instagram.com"),
        "open reddit": ("Opening Reddit", "https://www.reddit.com"),
        "open spotify": ("Opening Spotify", "https://open.spotify.com"),
        "open netflix": ("Opening Netflix", "https://www.netflix.com"),
        "open amazon": ("Opening Amazon", "https://www.amazon.com"),
        "open wikipedia": ("Opening Wikipedia", "https://www.wikipedia.org"),
        "open stack overflow": ("Opening Stack Overflow", "https://stackoverflow.com"),
        "open stackoverflow": ("Opening Stack Overflow", "https://stackoverflow.com"),
        "open discord": ("Opening Discord", "https://discord.com"),
        "open whatsapp": ("Opening WhatsApp", "https://web.whatsapp.com"),
        "open gmail": ("Opening Gmail", "https://mail.google.com"),
        "open google maps": ("Opening Google Maps", "https://maps.google.com"),
        "open tiktok": ("Opening TikTok", "https://www.tiktok.com"),
        "open pinterest": ("Opening Pinterest", "https://www.pinterest.com"),
        "open twitch": ("Opening Twitch", "https://www.twitch.tv"),
        "open medium": ("Opening Medium", "https://medium.com"),
        "open notion": ("Opening Notion", "https://www.notion.so"),
        "open figma": ("Opening Figma", "https://www.figma.com"),
        "open canva": ("Opening Canva", "https://www.canva.com"),
        "open zoom": ("Opening Zoom", "https://zoom.us"),
        "open google drive": ("Opening Google Drive", "https://drive.google.com"),
        "open google docs": ("Opening Google Docs", "https://docs.google.com"),
        "open google sheets": ("Opening Google Sheets", "https://sheets.google.com"),
        "open google slides": ("Opening Google Slides", "https://slides.google.com"),
        "open calendar": ("Opening Google Calendar", "https://calendar.google.com"),
        "open google calendar": ("Opening Google Calendar", "https://calendar.google.com"),
        "open translate": ("Opening Google Translate", "https://translate.google.com"),
        "open google translate": ("Opening Google Translate", "https://translate.google.com"),
        "open weather": ("Opening Weather", "https://www.google.com/search?q=weather"),
    }
    for key, (msg, url) in site_map.items():
        if key in c:
            return {"response": msg, "action": "open_url", "url": url}

    # Search Google
    if c.startswith("search") or c.startswith("google"):
        query = c.replace("search", "").replace("google", "").strip()
        if query:
            return {"response": "Searching Google for: {}".format(query),
                    "action": "open_url",
                    "url": "https://www.google.com/search?q={}".format(query.replace(' ', '+'))}

    # Play music
    if c.startswith("play"):
        parts = c.split(" ", 1)
        song = parts[1].strip() if len(parts) > 1 else ""
        link = music.get(song)
        if link:
            return {"response": "Playing {}".format(song.title()), "action": "open_url", "url": link}
        else:
            available = ", ".join(list(music.keys())[:10])
            return {"response": "Sorry, I couldn't find '{}'. Try: {}".format(song, available)}

    if "list songs" in c or "show songs" in c or "music library" in c:
        songs = ", ".join(music.keys())
        return {"response": "Available songs: {}".format(songs)}

    # Joke
    if "joke" in c or "funny" in c or "laugh" in c:
        return {"response": pyjokes.get_joke()}

    # Time
    if "time" in c:
        for prep in [" in ", " of ", " at ", " for "]:
            if prep in c:
                place = c.split(prep, 1)[1].strip()
                tz = get_timezone_from_place(place)
                if tz:
                    t = datetime.datetime.now(pytz.timezone(tz))
                    return {"response": "The time in {} is {} ({})".format(
                        place.title(), t.strftime('%I:%M %p'), t.strftime('%A, %B %d'))}
                else:
                    return {"response": "Sorry, I don't know the timezone for '{}'. Try major cities like London, Tokyo, Dubai.".format(place)}
        now = datetime.datetime.now()
        return {"response": "Local time is {} on {}".format(now.strftime('%I:%M %p'), now.strftime('%A, %B %d, %Y'))}

    # Date
    if "date" in c:
        for prep in [" in ", " of ", " at ", " for "]:
            if prep in c:
                place = c.split(prep, 1)[1].strip()
                tz = get_timezone_from_place(place)
                if tz:
                    d = datetime.datetime.now(pytz.timezone(tz))
                    return {"response": "The date in {} is {}".format(place.title(), d.strftime('%A, %B %d, %Y'))}
                else:
                    return {"response": "Sorry, I don't know the timezone for '{}'.".format(place)}
        now = datetime.datetime.now()
        return {"response": "Today is {}".format(now.strftime('%A, %B %d, %Y'))}

    # Weather
    if "weather" in c:
        for prep in [" in ", " at ", " for "]:
            if prep in c:
                city = c.split(prep, 1)[1].strip()
                return get_weather(city)
        return {"response": "Please specify a city. Try: 'weather in London' or 'weather in Dubai'"}

    # News
    if "news" in c or "headlines" in c or "latest news" in c:
        NEWS_API_KEY = "YOUR_NEWSAPI_KEY"  # Replace with your NewsAPI key
        try:
            url = "https://newsapi.org/v2/top-headlines?country=us&apiKey={}".format(NEWS_API_KEY)
            r = req.get(url, timeout=5)
            data = r.json()
            titles = [a["title"] for a in data.get("articles", [])[:6]]
            if titles:
                headlines = "\n".join("- {}".format(t) for t in titles)
                return {"response": "Latest Headlines:\n{}".format(headlines)}
            else:
                return {"response": "Couldn't fetch news. Please check your News API key."}
        except Exception:
            return {"response": "News API error. Add your NewsAPI key in app.py to get live news."}

    # Math
    if any(op in c for op in ["+", "-", "*", "/", "times", "plus", "minus", "divided"]):
        try:
            expr = c.replace("times", "*").replace("plus", "+").replace("minus", "-").replace("divided by", "/").replace("divided", "/")
            nums = re.findall(r"\d+", expr)
            if len(nums) >= 2:
                n1, n2 = int(nums[0]), int(nums[1])
                if "+" in expr or "plus" in c:
                    return {"response": "{} + {} = {}".format(n1, n2, n1 + n2)}
                elif "-" in expr or "minus" in c:
                    return {"response": "{} - {} = {}".format(n1, n2, n1 - n2)}
                elif "*" in expr or "times" in c:
                    return {"response": "{} x {} = {}".format(n1, n2, n1 * n2)}
                elif "/" in expr or "divided" in c:
                    if n2 != 0:
                        return {"response": "{} / {} = {:.2f}".format(n1, n2, n1 / n2)}
                    else:
                        return {"response": "Cannot divide by zero!"}
        except Exception:
            pass

    # Fact
    if "fact" in c or "trivia" in c:
        facts = [
            "Sharks have been around for over 400 million years -- longer than trees!",
            "The human brain uses about 20% of the body's total energy.",
            "Honey never spoils. Archaeologists found 3,000-year-old honey still edible!",
            "Octopuses have three hearts and blue blood.",
            "The Eiffel Tower grows taller in summer due to thermal expansion.",
            "Bananas are berries, but strawberries are not!",
            "A day on Venus is longer than a year on Venus.",
            "Wombat poop is cube-shaped.",
            "The Great Wall of China is not visible from space with the naked eye.",
            "Butterflies taste with their feet.",
        ]
        return {"response": "Did you know? {}".format(random.choice(facts))}

    # Motivation
    if "motivate" in c or "motivation" in c or "inspire" in c or "quote" in c:
        quotes = [
            "The only way to do great work is to love what you do. -- Steve Jobs",
            "Believe you can and you're halfway there. -- Theodore Roosevelt",
            "Don't watch the clock; do what it does. Keep going. -- Sam Levenson",
            "The future belongs to those who believe in the beauty of their dreams. -- Eleanor Roosevelt",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. -- Winston Churchill",
            "Your time is limited, don't waste it living someone else's life. -- Steve Jobs",
            "Everything you've ever wanted is on the other side of fear. -- George Addair",
        ]
        return {"response": random.choice(quotes)}

    # Exit
    if "stop" in c or "exit" in c or "goodbye" in c or "bye" in c:
        return {"response": "Goodbye! Swim safe and come back anytime!", "action": "exit"}

    # Help
    if "help" in c or "what can you do" in c or "commands" in c:
        return {"response": (
            "Here is what I can do:\n\n"
            "- Open websites (Google, YouTube, GitHub, etc.)\n"
            "- Play music from the library\n"
            "- Check time & date worldwide\n"
            "- Tell jokes\n"
            "- Fetch news (needs API key)\n"
            "- Basic math\n"
            "- Random facts\n"
            "- Motivational quotes\n"
            "- Weather info\n\n"
            "Just type or speak your command!"
        )}

    # Fallback
    return {"response": "I heard: \"{}\" -- but I'm not sure what to do. Try: 'help' to see what I can do!".format(c)}


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"response": "I didn't catch that. Please try again."})
    result = process_command(text)
    return jsonify(result)

@app.route("/status")
def status():
    return jsonify({"status": "Shark is online", "time": datetime.datetime.now().strftime("%I:%M %p")})

@app.route("/songs")
def songs():
    return jsonify({"songs": list(music.keys())})

if __name__ == "__main__":
    print("Shark Assistant running at http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)