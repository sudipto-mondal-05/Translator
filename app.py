from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import speech_recognition as sr
import time  # To create unique filenames for audio

app = Flask(__name__)

# Function to translate English text to Bengali
def translate_text(text):
    return GoogleTranslator(source="en", target="bn").translate(text)

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("✅ Recognized Speech:", text)
        return text
    except sr.UnknownValueError:
        return "⚠️ Sorry, I couldn't understand your speech."
    except sr.RequestError:
        return "⚠️ Error connecting to the speech recognition service."

# Flask Route: Home Page
@app.route("/", methods=["GET", "POST"])
def home():
    translated_text = ""
    audio_file = ""

    if request.method == "POST":
        input_text = request.form.get("text", "")  # Get text input
        if not input_text:
            input_text = speech_to_text()  # If no text, get voice input

        translated_text = translate_text(input_text)  # Translate text

        # Create a unique filename using timestamp to prevent caching issues
        unique_filename = f"static/output_{int(time.time())}.mp3"
        tts = gTTS(text=translated_text, lang='bn')
        tts.save(unique_filename)

        # Assign the new file to be played
        audio_file = unique_filename

    return render_template("index.html", translated_text=translated_text, audio_file=audio_file)

# Flask Route: Handle Voice Input
@app.route("/voice", methods=["POST"])
def voice():
    spoken_text = speech_to_text()
    return jsonify({"spoken_text": spoken_text})

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
