import os
from pydub import AudioSegment
from loguru import logger
from typing import Optional

def convert_to_wav(input_path: str, output_path: Optional[str] = None) -> str:
    """Convert audio file to WAV format (16kHz, mono)"""
    try:
        if output_path is None:
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}_converted.wav"
        
        logger.info(f"Converting {input_path} to WAV format")
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(output_path, format="wav")
        return output_path
    
    except Exception as e:
        logger.error(f"Audio conversion error: {e}")
        raise

def validate_audio_duration(audio_path: str, max_duration: int = 30) -> bool:
    """Validate audio duration doesn't exceed limit"""
    try:
        audio = AudioSegment.from_file(audio_path)
        duration = len(audio) / 1000
        return duration <= max_duration
    except Exception as e:
        logger.error(f"Duration validation error: {e}")
        raise