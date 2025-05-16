from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict
from main import process_audio  # Your custom function
from loguru import logger

# Setup
app = FastAPI(title="Speech Recognition WebApp")
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/recognize")
async def recognize_speech(audio: UploadFile = File(...), method: str = "both") -> Dict[str, str]:
    """
    Recognize speech from uploaded audio file.
    """
    try:
        if not audio.filename.lower().endswith(('.mp3', '.wav')):
            raise HTTPException(status_code=400, detail="Only MP3 or WAV files are supported")

        session_id = str(uuid.uuid4())
        upload_path = f"uploads/{session_id}_{audio.filename}"
        output_dir = f"outputs/{session_id}"
        os.makedirs(output_dir, exist_ok=True)

        with open(upload_path, "wb") as buffer:
            buffer.write(await audio.read())

        logger.info(f"Processing uploaded file: {upload_path}")
        results = process_audio(upload_path, method)

        result_file = f"{output_dir}/results.txt"
        with open(result_file, "w") as f:
            f.write(f"Results for {audio.filename}\n\n")
            if results.get("google"):
                f.write("Google Results:\n")
                f.write(results["google"] + "\n\n")
            if results.get("wav2vec2"):
                f.write("Wav2Vec2 Results:\n")
                f.write(results["wav2vec2"] + "\n")

        return JSONResponse({
            "status": "success",
            "result_id": session_id,
            **results
        })

    except Exception as e:
        logger.exception("Failed to recognize speech.")
        raise HTTPException(status_code=500, detail=f"Speech recognition failed: {str(e)}")


@app.get("/download/{result_id}")
async def download_results(result_id: str):
    result_file = f"outputs/{result_id}/results.txt"
    if not os.path.exists(result_file):
        raise HTTPException(404, detail="Results not found")
    return FileResponse(result_file, filename="speech_results.txt")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
