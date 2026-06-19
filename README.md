# 🦈 SharkAssistant: Python-Based Virtual Voice Assistant

A lightweight, localized Python voice assistant designed to process spoken user commands, perform automated web actions, retrieve system/timezone info, and provide real-time audio responses. Built using offline Text-to-Speech (TTS) pipelines and localized Speech-to-Text (STT) engines.

---

## 🚀 Key Feature Set

### 1. 🎙️ Localized Speech-to-Text (STT)
- **Voice Parsing:** Uses the `SpeechRecognition` engine to capture localized microphone inputs, translating spoken commands dynamically into clean string queries [3].
- **Microphone Management:** Integrates with `pyaudio` to manage physical microphone hardware channels with low latency [3].

### 2. 🗣️ Offline Text-to-Speech (TTS)
- **Offline Voice Engine:** Powered by `pyttsx3` to provide instant vocal feedback and responses without relying on an internet connection or cloud-based text-to-speech APIs.
- **Customizable Playback:** Adjusts speech rate (speed) and volume properties programmatically to optimize conversational clarity.

### 3. 🌐 Automated Web Operations
- **Browser Automation:** Dynamically opens custom web search strings on Google and YouTube.
- **API Queries:** Integrates Wikipedia query parsers to fetch and read aloud summarized search explanations on-demand.

### 4. 🎵 Localized Music Library Mappings
- **Custom Playlist Mappings:** References a separate, user-defined local module (`musiclibrary.py`) containing a dictionary of song titles mapped to YouTube URLs.
- **Vocal Triggers:** Detects the command "play [song_name]" and instantly launches the corresponding video in your default browser.

### 5. ⏰ System & Timezone Utilities
- **Pytz Integration:** Supports timezone-specific queries, enabling the assistant to calculate and report the current hour for customized geographic zones.
- **System Commands:** Accesses baseline system paths to run files or retrieve local clock data.

### 6. 🃏 Entertainment (PyJokes)
- **Developer Humor:** Calls the `pyjokes` library to retrieve and read aloud randomized programming and systems jokes.

---

## 🛠️ Technology Stack & Dependencies

- **Language:** Python 3.x
- **Key Packages:**
  - `SpeechRecognition` (Audio parsing engine)
  - `pyaudio` (Microphone stream accessor) [3]
  - `pyttsx3` (Offline text-to-speech converter)
  - `requests` (Web API client)
  - `pyjokes` (Joke generator)
  - `pytz` (Timezone database)

---

## 📁 File Architecture

1. **`sharkassistant.py`**: The primary executable engine containing the main listening loop, speech conversion settings, and conditional command processor logic.
2. **`musiclibrary.py`**: A localized module containing a dictionary of mapped songs and YouTube links:
   ```python
   music = {
       "skyfall": "https://www.youtube.com/watch?v=DeumyOzKqgI",
       "perfect": "https://www.youtube.com/watch?v=2Vv-BfVoq4g"
   }
