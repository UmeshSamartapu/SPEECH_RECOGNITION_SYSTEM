# 🎤 Speech Recognition System

A complete Python-based system for transcribing speech to text using two approaches:
1. **Google Web Speech API** (via `speechrecognition`)
2. **Facebook's Wav2Vec2** (via Hugging Face Transformers)

![Frontend](https://github.com/UmeshSamartapu/SPEECH_RECOGNITION_SYSTEM/blob/main/App/input/speechrecogwithGoogle-Frontend.png)

## 🌟 Features
- Supports both Google API and Wav2Vec2 models
- Audio preprocessing (MP3 → WAV conversion, trimming)
- CLI and FastAPI web interface
- Logging and error handling
- Max 30-second audio input limitation

## 📂 Directory Structure
```bash
speech-recognition-system/
├── main.py # Main CLI interface
├── api.py # FastAPI web server
├── audio_processing.py # Audio conversion/trimming
├── google_speech_recognition.py # Google API implementation
├── wav2vec2_recognition.py # Wav2Vec2 implementation
├── requirements.txt # Dependencies
├── tests/
│ └── test_audio.mp3 # Sample audio
├── static/
│ ├── style.css # Frontend CSS
│ └── script.js # Frontend JS
├── templates/
│ └── index.html # Web interface
├── uploads/ # Auto-created for user uploads
└── outputs/ # Auto-created for transcripts
```

## 🛠 Installation
```bash
# Clone repository
git clone https://github.com/yourusername/speech-recognition-system.git
cd speech-recognition-system
```

# Install dependencies
```bash
pip install -r requirements.txt
```
## 🚀 Usage

### CLI Mode
```bash
# Process audio with both methods
python main.py "tests/test_audio.mp3" --method both

# Use specific method (google/wav2vec2/both)
python main.py "path/to/audio.mp3" --method wav2vec2
```
### Web Interface

```bash
uvicorn api:app --reload
```

### Open http://127.0.0.1:8000 in your browser.
```bash
http://localhost:8000
```

## 🔧 Dependencies
Listed in **requirements.txt**
```bash
fastapi==0.95.2
uvicorn==0.22.0
speechrecognition==3.10.0
pydub==0.25.1
transformers==4.36.2
torch==2.1.1
librosa==0.10.1
soundfile==0.12.1
python-multipart==0.0.6
python-dotenv==1.0.0
loguru==0.7.2
jinja2==3.1.2
```

## 📖 Documentation

### Audio Processing
- Converts MP3 to WAV using pydub
- Trims audio to 30 seconds max
- Sample rate normalization

### Recognition Methods
```bash
| Method     | Accuracy | Internet Required | Speed |
|------------|----------|-------------------|-------|
| Google API | Medium   | Yes               | Fast  |
| Wav2Vec2   | High     | No                | Slow  |
```

## 🌐 API Endpoints
- **POST /upload:** Upload audio file
- **GET /results:** Get transcription
- **POST /process:** Direct processing

## 🧪 Testing
```bash
python main.py "tests/test_audio.mp3" --method both
```

### License
This project is licensed under the MIT License - see the LICENSE file for details.

## Demo 
### You can watch the ([youtube video](  )) for demo
<p align="center">
  <img src="https://github.com/UmeshSamartapu/SPEECH_RECOGNITION_SYSTEM/blob/main/App/input/speechrecogwithGoogle-Demo.gif" />
</p>  


## 📫 Let's Connect

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/umeshsamartapu/)
[![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat-square&logo=twitter&logoColor=white)](https://x.com/umeshsamartapu)
[![Email](https://img.shields.io/badge/-Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:umeshsamartapu@gmail.com)
[![Instagram](https://img.shields.io/badge/-Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/umeshsamartapu/)
[![Buy Me a Coffee](https://img.shields.io/badge/-Buy%20Me%20a%20Coffee-FBAD19?style=flat-square&logo=buymeacoffee&logoColor=black)](https://www.buymeacoffee.com/umeshsamartapu)

---

🔥 Always exploring new technologies and solving real-world problems with code!
