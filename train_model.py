import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os

# Simulate training data
data = pd.DataFrame({
    "mfcc_1": np.random.rand(100),
    "mfcc_2": np.random.rand(100),
    "mfcc_3": np.random.rand(100),
    "pitch": np.random.uniform(80, 300, 100),
    "jitter": np.random.rand(100),
    "shimmer": np.random.rand(100),
    "hnr": np.random.uniform(10, 30, 100),
    "label": np.random.choice(["Healthy", "Diseased"], 100)
})

# Split features and labels
X = data.drop("label", axis=1)
y = data["label"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = RandomForestClassifier()
model.fit(X_scaled, y)

# Save model
os.makedirs("models", exist_ok=True)
with open("models/rf_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved as models/rf_model.pkl")

# Test the saved model
model = pickle.load(open("models/rf_model.pkl", "rb"))
print(model.predict([[0.1, 0.2, 0.3, 150, 0.01, 0.02, 20]]))