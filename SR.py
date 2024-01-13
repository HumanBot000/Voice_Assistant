import time
import pyttsx3
import speech_recognition as sr
from threading import Thread

recognized_text = ""  # Globale Variable zum Speichern des erkannten Texts

def listen_for_speech(recognizer, microphone):
    global recognized_text  # Zugriff auf die globale Variable
    print("Listening for speech...")
    while True:
        with microphone as source:
            try:
                audio_data = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio_data, language="de-De")
                if text:
                    recognized_text = text  # Aktualisiere die globale Variable
                    print("Recognized:", text)
            except sr.UnknownValueError:
                pass  # Ignore unrecognized speech
            except sr.RequestError as e:
                print(f"Google API request failed; {e}")

def process_recognized_text():
    global recognized_text  # Zugriff auf die globale Variable
    while True:
        if recognized_text:
            # Hier können Sie den erkannten Text weiterverarbeiten
            print("Processing:", recognized_text)
            recognized_text = ""  # Zurücksetzen des erkannten Texts

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    engine = pyttsx3.init()
    engine.say("Start")
    engine.runAndWait()

    # Starten Sie die Threads
    listen_thread = Thread(target=listen_for_speech, args=(recognizer, microphone), daemon=True)
    process_thread = Thread(target=process_recognized_text, daemon=True)
    listen_thread.start()
    process_thread.start()

    try:
        while True:
            # Ihr Hauptthread kann andere Aufgaben hier erledigen
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated by user.")
