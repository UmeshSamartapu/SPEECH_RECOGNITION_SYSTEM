import argparse
import os
import shutil
from datetime import datetime
from loguru import logger
from audio_processing import convert_to_wav, validate_audio_duration
from google_speech_recognition import recognize_with_google
from wav2vec2_recognition import recognize_with_wav2vec2

# Configure output directory
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_results(audio_path, results, log_content):
    """Save all outputs to a separate output subdirectory for each audio"""
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    subfolder_name = f"{base_name}_{timestamp}"
    subfolder_path = os.path.join(OUTPUT_DIR, subfolder_name)
    os.makedirs(subfolder_path, exist_ok=True)

    # Save a copy of the original audio
    audio_ext = audio_path.split('.')[-1]
    audio_copy = f"{base_name}_input.{audio_ext}"
    shutil.copy(audio_path, os.path.join(subfolder_path, audio_copy))

    # Save converted WAV if different from original
    if not audio_path.lower().endswith('.wav'):
        wav_path = convert_to_wav(audio_path)
        wav_copy = f"{base_name}_converted.wav"
        shutil.copy(wav_path, os.path.join(subfolder_path, wav_copy))

    # Save results to text file
    result_file = f"{base_name}_results.txt"
    result_file_path = os.path.join(subfolder_path, result_file)
    with open(result_file_path, 'w') as f:
        f.write(f"Processing results for {audio_path}\n")
        f.write(f"Processing time: {timestamp}\n\n")

        if results.get("google"):
            f.write("[GOOGLE WEB SPEECH API]\n")
            f.write("="*50 + "\n")
            f.write(results["google"] + "\n\n")

        if results.get("wav2vec2"):
            f.write("[WAV2VEC2]\n")
            f.write("="*50 + "\n")
            f.write(results["wav2vec2"] + "\n\n")

    # Save full log
    log_file = f"{base_name}_log.log"
    log_file_path = os.path.join(subfolder_path, log_file)
    with open(log_file_path, 'w') as f:
        f.write(log_content)

    return result_file_path  # full path


def process_audio(input_path: str, method: str = "both") -> dict:
    """Process audio file with specified recognition method(s)"""
    results = {}

    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Audio file not found: {input_path}")

        if not input_path.lower().endswith('.wav'):
            logger.info("Converting to WAV...")
            input_path = convert_to_wav(input_path)

        if not validate_audio_duration(input_path):
            raise ValueError("Audio duration exceeds 30 seconds limit")

        if method in ["google", "both"]:
            logger.info("Running Google recognition...")
            results["google"] = recognize_with_google(input_path)

        if method in ["wav2vec2", "both"]:
            logger.info("Running Wav2Vec2 recognition...")
            results["wav2vec2"] = recognize_with_wav2vec2(input_path)

        return results

    except Exception as e:
        logger.error(f"Processing error: {e}")
        raise


def main():
    """Command-line interface for the speech recognition system"""
    parser = argparse.ArgumentParser(description="Speech Recognition System")
    parser.add_argument("audio_path", help="Path to audio file (MP3 or WAV)")
    parser.add_argument("--method", choices=["google", "wav2vec2", "both"],
                        default="both", help="Recognition method to use")

    args = parser.parse_args()

    # Set up logging to capture all output
    log_content = []
    logger.add(lambda msg: log_content.append(msg), level="INFO")

    try:
        logger.info(f"Starting processing for {args.audio_path}")
        results = process_audio(args.audio_path, args.method)

        # Save all outputs and get result file path
        result_path = save_results(args.audio_path, results, "\n".join(log_content))

        # Print final results to console
        print("\n" + "="*50)
        print(" PROCESSING COMPLETE ".center(50, "="))
        print("="*50)
        print(f"\nResults saved to: {result_path}")

        if results.get("google"):
            print("\n[GOOGLE WEB SPEECH API]")
            print("-"*50)
            print(results["google"])

        if results.get("wav2vec2"):
            print("\n[WAV2VEC2]")
            print("-"*50)
            print(results["wav2vec2"])

        print("\n" + "="*50)
        logger.success("Processing completed successfully")

    except Exception as e:
        logger.error(f"Processing failed: {e}")
        print(f"\nERROR: {e}")
        print("Check output directory for detailed logs")


if __name__ == "__main__":
    main()
