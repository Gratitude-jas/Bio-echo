from fastapi import APIRouter
from app.services.model import load_model  # adjust if needed


router = APIRouter()

# Load your trained model (e.g., RandomForest)
model = load_model()  # This should return a scikit-learn model

@router.post("/predict/")
def predict(features: dict):
    prediction = model.predict([list(features.values())])
    return {"parkinson_detected": bool(prediction[0])}