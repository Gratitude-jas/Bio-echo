
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes import upload, predict_route
from app.services.preprocess import preprocess_audio
import os
import shutil

app = FastAPI()

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/audio", StaticFiles(directory="frontend"), name="static")

# ✅ Include routers
app.include_router(upload.router)
app.include_router(predict_route.router)

# ✅ Root route
@app.get("/")
def read_root():
    return {"message": "BioEcho API is running"}


# ✅ Audio preprocessing route
@app.post("/process/")
def process_audio(filename: str):
    raw_path = os.path.join("data/raw", filename)
    cleaned_path = os.path.join("data/cleaned", filename)
    preprocess_audio(raw_path, cleaned_path)
    return {"message": "Audio processed", "cleaned_path": cleaned_path}

# ✅ Chart serving route
@app.get("/charts/{name}")
def get_chart(name: str):
    file_path = f"data/{name}.png"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Chart not found")

@app.get("/audio/{filename}")
def get_audio(filename: str):
    filepath = os.path.join("audio", filename)
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(filepath, media_type="audio/wav")
