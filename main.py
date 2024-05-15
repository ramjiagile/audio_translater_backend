from typing import Union
from fastapi import FastAPI
# Importing necessary modules required 
from playsound import playsound 
import speech_recognition as sr 
from googletrans import Translator 
from translate import Translator
from gtts import gTTS 
import os 

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/translate-audio")
def get_translate():
    flag = 0
    
    r = sr.Recognizer() 

    file_path = "sample-1.wav"
    text = convert_audio_to_text(file_path)

    # invoking Translator 
    translator= Translator(to_lang="Tamil")
    text_to_translate = translator.translate(text)

    speak = gTTS(text=text_to_translate, lang="ta")

    speak.save("captured_voice.mp3") 

    return text_to_translate
    
def convert_audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)  # Read the entire audio file

        text = recognizer.recognize_google(audio_data)  # Recognize speech using Google Speech Recognition
        return text
    except Exception as e:
        print("Error:", e)
        return None