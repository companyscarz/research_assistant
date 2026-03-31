#pip install pyttsx3
import pyttsx3

engine = pyttsx3.init() # object creation

def change_rate(rate_num: int):
    engine.setProperty('rate', rate_num)

def speak_out(text: str):
    engine.say(text)
    engine.runAndWait()

def stop_speech():
    engine.stop()

def change_voice(voice_index: int):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_index].id)

def is_speaking():
    return engine.isBusy()

def save_speech(text: str, file_name: str):
    engine.save_to_file(text , f'{file_name}.mp3')
