import torch
import librosa
import soundfile as sf
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from loguru import logger
from typing import Optional

# Load model and processor globally to avoid reloading
MODEL_NAME = "facebook/wav2vec2-base-960h"
processor = None
model = None

def load_wav2vec2_model():
    """Load Wav2Vec2 model and processor if not already loaded."""
    global processor, model
    if processor is None or model is None:
        logger.info(f"Loading Wav2Vec2 model: {MODEL_NAME}")
        processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME)
        model = Wav2Vec2ForCTC.from_pretrained(MODEL_NAME)
        logger.success("Model loaded successfully")

def recognize_with_wav2vec2(audio_path: str) -> Optional[str]:
    """
    Perform speech recognition using Facebook's Wav2Vec2 model.
    
    Args:
        audio_path: Path to WAV audio file
        
    Returns:
        Recognized text or None if recognition fails
    """
    try:
        load_wav2vec2_model()
        
        logger.info(f"Processing audio file: {audio_path}")
        
        # Load audio file
        speech, sample_rate = librosa.load(audio_path, sr=16000)
        
        # Tokenize
        input_values = processor(speech, sampling_rate=sample_rate, return_tensors="pt").input_values
        
        # Get logits
        with torch.no_grad():
            logits = model(input_values).logits
        
        # Get predicted ids
        predicted_ids = torch.argmax(logits, dim=-1)
        
        # Decode
        text = processor.batch_decode(predicted_ids)[0]
        
        logger.success("Wav2Vec2 recognition successful")
        return text
    
    except Exception as e:
        logger.error(f"Error during Wav2Vec2 recognition: {e}")
        return None
