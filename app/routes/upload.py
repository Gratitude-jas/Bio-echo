from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import csv
from datetime import datetime
from app.services.extract_features import extract_features
from app.services.model import load_model

router = APIRouter()

UPLOAD_DIR = "data/raw"
LOG_FILE = "data/predictions_log.csv"
os.makedirs(UPLOAD_DIR, exist_ok=True)

model = load_model()

@router.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        features = extract_features(file_path)
        feature_values = list(features.values())

        prediction = model.predict([feature_values])[0]
        confidence = model.predict_proba([feature_values])[0][int(prediction)]
        timestamp = datetime.now().isoformat()

        # Log to CSV
        log_exists = os.path.exists(LOG_FILE)
        with open(LOG_FILE, mode="a", newline="") as log_file:
            writer = csv.writer(log_file)
            if not log_exists:
                writer.writerow(["filename", *features.keys(), "parkinson_detected", "confidence", "timestamp"])
            writer.writerow([file.filename, *feature_values, bool(prediction), round(confidence, 4), timestamp])
        print("Prediction:", prediction)
        print("Confidence:", confidence)
        print("Returning response...")

        return {
            "message": "File uploaded, features extracted, prediction complete",
            "filename": file.filename,
            "features": features,
            "parkinson_detected": bool(prediction),
            "confidence": round(confidence, 4)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during upload or prediction: {str(e)}")