import speech_recognition as sr
from loguru import logger
from typing import Optional

def recognize_with_google(audio_path: str, language: str = "en-US") -> Optional[str]:
    """
    Perform speech recognition using Google Web Speech API.
    
    Args:
        audio_path: Path to WAV audio file
        language: Language code for recognition (default: en-US)
        
    Returns:
        Recognized text or None if recognition fails
    """
    try:
        logger.info(f"Initializing Google Web Speech API recognizer for {audio_path}")
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Load audio file
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        
        logger.info("Performing speech recognition...")
        
        # Use Google Web Speech API
        text = recognizer.recognize_google(audio_data, language=language)
        
        logger.success("Recognition successful")
        return text
    
    except sr.UnknownValueError:
        logger.error("Google Web Speech API could not understand audio")
    except sr.RequestError as e:
        logger.error(f"Could not request results from Google Web Speech API; {e}")
    except Exception as e:
        logger.error(f"Error during Google speech recognition: {e}")
    
    return None
