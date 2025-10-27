'''from fastapi import FastAPI
from app.routes import upload, predict_route
from app.services.preprocess import preprocess_audio
import os

app = FastAPI()
app.include_router(upload.router)
app.include_router(predict_route.router)  # ✅ Add this line

@app.get("/")
def read_root():
    return {"message": "BioEcho API is running"}

@app.post("/process/")
def process_audio(filename: str):
    raw_path = os.path.join("data/raw", filename)
    cleaned_path = os.path.join("data/cleaned", filename)
    preprocess_audio(raw_path, cleaned_path)
    return {"message": "Audio processed", "cleaned_path": cleaned_path}

from fastapi.responses import FileResponse
from fastapi import HTTPException
import os

@app.get("/charts/{name}")
def get_chart(name: str):
    file_path = f"data/{name}.png"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Chart not found")

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    # Dummy response for testing

    print(f"Received file: {file.filename}")
    return {
        "parkinson_detected": True,
        "confidence": 0.87
    }'''

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
app.mount("/static", StaticFiles(directory="frontend"), name="static")

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

# # ✅ Upload route (directly in main if not using router)
# @app.post("/upload/")
# async def upload_audio(file: UploadFile = File(...)):
#     upload_dir = "data/raw"
#     os.makedirs(upload_dir, exist_ok=True)
#     file_path = os.path.join(upload_dir, file.filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     print(f"Received file: {file.filename}")

#     # TODO: Replace with actual prediction logic
#     prediction = True if "B2L" in file.filename else False
#     confidence = 0.87 if prediction else 0.42

#     return {
#         "parkinson_detected": prediction,
#         "confidence": confidence
#     }