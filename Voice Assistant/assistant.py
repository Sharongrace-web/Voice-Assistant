import speech_recognition as sr
import pyttsx3
import datetime
import requests

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Lists & API Keys
reminders = []
WEATHER_API_KEY = "707216a451553ffe8432befac7ab11bb"  # Replace with your OpenWeatherMap API key
NEWS_API_KEY = "88b4317ff7a74d87be680ec4a711c3e6"        # Replace with your NewsAPI key

# Text-to-speech function
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to capture voice commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Network error.")
            return ""

# Function to handle reminders
def handle_reminders(command):
    global reminders

    if "reminder" in command and "to" in command:
        reminder = command.split("to", 1)[1].strip()
        time = datetime.datetime.now().strftime("%H:%M:%S")
        reminders.append((reminder, time))
        speak(f"Reminder added: {reminder}")

    elif "what are my reminders" in command:
        if reminders:
            speak("Here are your reminders:")
            for rem, time in reminders:
                speak(f"At {time}, {rem}")
        else:
            speak("You don't have any reminders.")

    elif "clear reminders" in command or "delete all reminders" in command:
        reminders.clear()
        speak("All reminders have been cleared.")

# Function to get weather info
def get_weather(command):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    if "in" in command:
        city_name = command.split("in", 1)[1].strip()
    else:
        speak("Please specify a city.")
        return

    complete_url = f"{base_url}appid={WEATHER_API_KEY}&q={city_name}&units=metric"

    try:
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            main = data["main"]
            temp = main["temp"]
            humidity = main["humidity"]
            weather_desc = data["weather"][0]["description"]

            weather_report = f"The weather in {city_name} is {weather_desc} with a temperature of {temp}°C and humidity of {humidity}%."
            speak(weather_report)
        else:
            speak("City not found.")
    except:
        speak("Unable to retrieve weather information.")

# Function to get top news headlines
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] == "ok":
            articles = data["articles"][:5]
            speak("Here are the top news headlines:")
            for i, article in enumerate(articles, 1):
                headline = article["title"]
                speak(f"Headline {i}: {headline}")
        else:
            speak("Unable to fetch news at the moment.")
    except:
        speak("Network error while fetching news.")

# Main program loop
if __name__ == "__main__":
    speak("Hello, I am your personal assistant. How can I help you?")
    while True:
        command = listen()

        if "stop" in command or "exit" in command:
            speak("Goodbye!")
            break
        elif "reminder" in command:
            handle_reminders(command)
        elif "weather" in command:
            get_weather(command)
        elif "news" in command:
            get_news()
        else:
            speak("Sorry, I didn't understand that.")