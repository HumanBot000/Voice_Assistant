import os
import re
import time

import gpt4all
import pyttsx3
import speech_recognition as sr
from threading import Thread

recognized_text = ""
system_prompt = "Du bist ein einfacher Sprachassistent. Antworte ausschließlich auf deutsch. Gebe kurze und kompakte Antworten zurück, da deine Antworten durch ein text to speech programm gesendet werden."
model_name = "mistral-7b-openorca.Q4_0.gguf"
model_path = f"{os.environ['LOCALAPPDATA']}\\nomic.ai\\GPT4All"

model = gpt4all.GPT4All(model_name, model_path=model_path)



def listen_for_speech(recognizer, microphone):
    global recognized_text
    while True:
        print("Listening...")
        with microphone as source:
            try:
                audio_data = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio_data, language="de-De")
                if text:
                    recognized_text = text
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Google API request failed; {e}")


def say(text, engine):
    engine.say(text)
    engine.runAndWait()


def process_command(command, tts_engine):
    start = time.time()
    command = re.sub(r"assistant", "", command)
    command = re.sub(r"assistent", "", command)
    command = command.strip()
    print(f"Processing: {command}")
    say("Befehl erfasst. Berechne...", tts_engine)
    with model.chat_session(system_prompt):
        response = model.generate(command)
    print(f"Assistant: {response}")
    say(response,tts_engine)
    print(f"Command finished-{time.time()-start} seconds")
    listen_thread.join()
    process_thread.join()
    listen_thread.start()
    process_thread.start()


def process_recognized_text(tts_engine):
    global recognized_text
    while True:
        if recognized_text:
            print("User:", recognized_text)
            if recognized_text.lower().startswith("assistant") or recognized_text.lower().startswith("assistent"):
                process_command(recognized_text, tts_engine)
            recognized_text = ""


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()
    say("start", engine)
    listen_thread = Thread(target=listen_for_speech, args=(recognizer, microphone), daemon=True)
    process_thread = Thread(target=process_recognized_text, daemon=True, args=(engine,))
    listen_thread.start()
    process_thread.start()
    while True:
        time.sleep(1)
