import speech_recognition as sr
import requests
import os
import pygame
import json
import ollama
from gtts import gTTS

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=7)

    try:
        request = recognizer.recognize_google(audio)
        print("You said : "+request )
        return request
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def text_to_speech(text):
    sound_file = 'speech.wav'
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(sound_file)
    play_audio(sound_file)
    
def play_audio(sound_file):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))

def getAiResponse(prompt):
    response = ollama.chat(model='phi', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])
    return (response['message']['content'])


if __name__ == '__main__':
    
    while True:
        voicemessage = recognize_speech()
        if voicemessage:
            response = getAiResponse(voicemessage)
            print(response)
            text_to_speech(response)
    
