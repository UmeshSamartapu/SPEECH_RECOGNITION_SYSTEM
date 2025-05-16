import os
from loguru import logger
from audio_processing import convert_to_wav, validate_audio_duration
from google_speech_recognition import recognize_with_google
from wav2vec2_recognition import recognize_with_wav2vec2

def process_audio(input_path: str, method: str = "both") -> dict:
    """Process audio file with specified recognition method(s)"""
    results = {}
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Audio file not found: {input_path}")
        
        if not input_path.lower().endswith('.wav'):
            input_path = convert_to_wav(input_path)
        
        if not validate_audio_duration(input_path):
            raise ValueError("Audio exceeds 30 second limit")
        
        if method in ["google", "both"]:
            results["google"] = recognize_with_google(input_path)
        
        if method in ["wav2vec2", "both"]:
            results["wav2vec2"] = recognize_with_wav2vec2(input_path)
        
        return results
    except Exception as e:
        logger.error(f"Processing error: {e}")
        raise