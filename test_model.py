import joblib
import numpy as np

# Load model
model = joblib.load("models/rf_model.pkl")

# Print model info
print("🧠 Model type:", type(model))
print("🔢 Classes:", model.classes_)
print("📊 Number of features expected:", model.n_features_in_)

# Create a test input (same format as your extracted features)
sample = [-462.60, 120.00, 80.39, 389.38, 0.445, 0.092, 53.36]  # Healthy sample

# Predict
prediction = model.predict([sample])[0]
proba = model.predict_proba([sample])[0]

print("🧪 Prediction:", prediction)
print("📈 Probabilities:", proba)