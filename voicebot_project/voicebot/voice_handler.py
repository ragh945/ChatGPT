import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import time
import tempfile

def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            return "Listening timed out."
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "API error."

def speak_text(text):
    # Ensure text is string, even if dict passed by mistake
    if isinstance(text, dict):
        text = str(text)

    try:
        tts = gTTS(text=text, lang='en')
        
        # Create a temporary file for the mp3
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name
        tts.save(temp_filename)

        # Initialize and use pygame to play audio
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.5)

    except Exception as e:
        print(f"[Error during speech synthesis or playback]: {e}")

    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass

        try:
            os.remove(temp_filename)
        except Exception as e:
            print(f"Error deleting temp file: {e}")
