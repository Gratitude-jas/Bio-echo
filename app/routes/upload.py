from fastapi import APIRouter, UploadFile, File, HTTPException
import os
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
        print("📥 File saved at:", file_path)

        # Extract features
        print("🔍 Starting feature extraction...")
        features = extract_features(file_path)
        print("✅ Features extracted:", features)

        feature_values = list(features.values())
        print("📊 Feature values:", feature_values)

        # Make prediction
        prediction = model.predict([feature_values])[0]
        print("🧠 Prediction:", prediction)

        class_index = list(model.classes_).index(prediction)
        print("🔢 Class index:", class_index)

        confidence = model.predict_proba([feature_values])[0][class_index]
        print("📈 Confidence:", confidence)

        timestamp = datetime.now().isoformat()

        # SHAP explainability
        explainer = shap.TreeExplainer(model)
        shap_input = np.array([feature_values])
        shap_values = explainer.shap_values(shap_input)[class_index]
        # feature_importance = dict(zip(features.keys(), shap_values))
        feature_importance = {
            key: float(value) if isinstance(value, (np.float32, np.float64, float)) else float(value[0])
            for key, value in zip(features.keys(), shap_values)
        }
        print("📌 Feature importance:", feature_importance)

        # Log to CSV
        log_exists = os.path.exists(LOG_FILE)
        with open(LOG_FILE, mode="a", newline="") as log_file:
            writer = csv.writer(log_file)
            if not log_exists:
                writer.writerow(["filename", *features.keys(), "parkinson_detected", "confidence", "timestamp"])
            writer.writerow([filename, *feature_values, bool(prediction == "Diseased"), round(confidence, 4), timestamp])

        print("✅ Returning response...")

        # Return full response
        return {
            "filename": filename,
            "parkinson_detected": bool(prediction == "Diseased"),
            "confidence": float(confidence),
            "features": features,
            "feature_importance": feature_importance
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error during upload or prediction: {str(e)}")