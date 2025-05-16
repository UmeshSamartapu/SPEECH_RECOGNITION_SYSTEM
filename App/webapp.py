from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uuid
from pathlib import Path
from main import process_audio
import logging

# Setup
app = FastAPI(title="Speech Recognition WebApp")
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Speech Recognition</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Speech Recognition</h1>
        <form id="uploadForm">
            <div class="form-group">
                <input type="file" id="audioFile" accept=".mp3,.wav" required>
            </div>
            <div class="form-group">
                <select id="method">
                    <option value="both">Both Methods</option>
                    <option value="google">Google</option>
                    <option value="wav2vec2">Wav2Vec2</option>
                </select>
            </div>
            <button type="submit">Process</button>
        </form>
        <div class="results" id="results"></div>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=html_template)

@app.post("/recognize")
async def recognize_speech(audio: UploadFile = File(...), method: str = "both"):
    try:
        # Generate unique ID for this session
        session_id = str(uuid.uuid4())
        upload_path = f"uploads/{session_id}_{audio.filename}"
        output_dir = f"outputs/{session_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            buffer.write(await audio.read())
        
        # Process audio
        results = process_audio(upload_path, method)
        
        # Save results to file
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
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/download/{result_id}")
async def download_results(result_id: str):
    result_file = f"outputs/{result_id}/results.txt"
    if not os.path.exists(result_file):
        raise HTTPException(404, detail="Results not found")
    return FileResponse(result_file, filename="speech_results.txt")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)