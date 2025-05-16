import torch
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from loguru import logger
from typing import Optional

MODEL_NAME = "facebook/wav2vec2-base-960h"
processor = None
model = None

def load_wav2vec2_model():
    """Load Wav2Vec2 model and processor"""
    global processor, model
    if processor is None or model is None:
        logger.info("Loading Wav2Vec2 model...")
        processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME)
        model = Wav2Vec2ForCTC.from_pretrained(MODEL_NAME)
        logger.success("Model loaded successfully")

def recognize_with_wav2vec2(audio_path: str) -> Optional[str]:
    """Perform speech recognition using Wav2Vec2"""
    try:
        load_wav2vec2_model()
        speech, sample_rate = librosa.load(audio_path, sr=16000)
        input_values = processor(speech, sampling_rate=sample_rate, return_tensors="pt").input_values
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        return processor.batch_decode(predicted_ids)[0]
    except Exception as e:
        logger.error(f"Wav2Vec2 recognition error: {e}")
        return None