import speech_recognition as sr
from loguru import logger
from typing import Optional

def recognize_with_google(audio_path: str, language: str = "en-US") -> Optional[str]:
    """Perform speech recognition using Google Web Speech API"""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data, language=language)
    except sr.UnknownValueError:
        logger.error("Google couldn't understand the audio")
    except sr.RequestError as e:
        logger.error(f"Google API error: {e}")
    except Exception as e:
        logger.error(f"Google recognition error: {e}")
    return None