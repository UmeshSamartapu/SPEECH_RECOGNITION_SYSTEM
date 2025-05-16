import os
from pydub import AudioSegment
from loguru import logger
from typing import Optional

def convert_to_wav(input_path: str, output_path: Optional[str] = None) -> str:
    """
    Convert audio file to WAV format (16kHz, mono) using pydub.
    
    Args:
        input_path: Path to input audio file
        output_path: Optional output path. If None, creates in same directory
        
    Returns:
        Path to converted WAV file
    """
    try:
        # Determine output path if not provided
        if output_path is None:
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}_converted.wav"
        
        logger.info(f"Converting {input_path} to WAV format at {output_path}")
        
        # Load audio file
        audio = AudioSegment.from_file(input_path)
        
        # Convert to mono and set frame rate to 16kHz (common for speech recognition)
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        # Export as WAV
        audio.export(output_path, format="wav")
        
        logger.success(f"Successfully converted to WAV: {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error converting audio: {e}")
        raise

def validate_audio_duration(audio_path: str, max_duration: int = 30) -> bool:
    """
    Validate that audio file doesn't exceed maximum duration.
    
    Args:
        audio_path: Path to audio file
        max_duration: Maximum allowed duration in seconds
        
    Returns:
        bool: True if audio is valid, False otherwise
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        duration = len(audio) / 1000  # pydub returns duration in milliseconds
        
        if duration > max_duration:
            logger.warning(f"Audio duration {duration}s exceeds maximum of {max_duration}s")
            return False
        
        logger.info(f"Audio duration valid: {duration}s")
        return True
    
    except Exception as e:
        logger.error(f"Error validating audio duration: {e}")
        raise
