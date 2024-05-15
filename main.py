from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
# Importing necessary modules required 
import speech_recognition as sr 
from googletrans import Translator 
from translate import Translator
from gtts import gTTS 
import os 

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/translate-audio")
def get_translate(file: UploadFile = File(...)):
    flag = 0

    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    
    r = sr.Recognizer() 

    # file_path = "sample-1.wav"
    file_path = file.filename
    text = convert_audio_to_text(file_path)

    # invoking Translator 
    translator= Translator(to_lang="Tamil")
    text_to_translate = translator.translate(text)

    speak = gTTS(text=text_to_translate, lang="ta")

    # saving the translated file
    translated_file_name = "captured_voice.mp3"

    speak.save(translated_file_name) 

    if not os.path.exists(translated_file_name):
        return {"error": "Translated file not found"}

    # Return the file for download
    return FileResponse(translated_file_name, filename=translated_file_name, media_type='application/octet-stream')
    
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