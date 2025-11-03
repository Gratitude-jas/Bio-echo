import joblib
import os

def load_model():
    base_dir = os.path.dirname(__file__)  # path to services/
    model_path = os.path.join(base_dir, "..", "models", "rf_model.pkl")
    model_path = os.path.abspath(model_path)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    return joblib.load(model_path)