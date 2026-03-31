#pip install speech_recognition
# pip install pyaudio

import speech_recognition as sr

#-----------audio to text---------
def detect_speech():
    recognizer =  sr.Recognizer() #initialize microphone
    microphone = sr.Microphone()
    with microphone as source: #audio source is microphone
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    #detect and return response
    speech_response = recognizer.recognize_google(audio)
    return speech_response

#speech = detect_speech()
#print(speech)
