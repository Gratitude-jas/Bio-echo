from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from fastapi.responses import JSONResponse
import csv
import numpy as np
from datetime import datetime
import shap
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
        # Save uploaded file
        filename = file.filename
        contents = await file.read()
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(contents)

        # Extract features
        features = extract_features(file_path)
        feature_values = list(features.values())

        # Make prediction
        prediction = model.predict([feature_values])[0]
        confidence = model.predict_proba([feature_values])[0][int(prediction)]
        timestamp = datetime.now().isoformat()

        # SHAP explainability
        explainer = shap.TreeExplainer(model)
        shap_input = np.array([feature_values])
        shap_values = explainer.shap_values(shap_input)[int(prediction)]
        feature_importance = dict(zip(features.keys(), shap_values))

        # Log to CSV
        log_exists = os.path.exists(LOG_FILE)
        with open(LOG_FILE, mode="a", newline="") as log_file:
            writer = csv.writer(log_file)
            if not log_exists:
                writer.writerow(["filename", *features.keys(), "parkinson_detected", "confidence", "timestamp"])
            writer.writerow([filename, *feature_values, bool(prediction), round(confidence, 4), timestamp])

        print("Prediction:", prediction)
        print("Confidence:", confidence)
        print("Returning response...")

        # Return full response
        return {
            "filename": filename,
            "parkinson_detected": bool(prediction),
            "confidence": float(confidence),
            "features": features,
            "feature_importance": feature_importance
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during upload or prediction: {str(e)}")