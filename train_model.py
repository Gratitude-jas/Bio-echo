# import pandas as pd
# import numpy as np
# import pickle
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler
# import os

# # Simulate training data
# data = pd.DataFrame({
#     "mfcc_1": np.random.rand(100),
#     "mfcc_2": np.random.rand(100),
#     "mfcc_3": np.random.rand(100),
#     "pitch": np.random.uniform(80, 300, 100),
#     "jitter": np.random.rand(100),
#     "shimmer": np.random.rand(100),
#     "hnr": np.random.uniform(10, 30, 100),
#     "label": np.random.choice(["Healthy", "Diseased"], 100)
# })

# # Split features and labels
# X = data.drop("label", axis=1)
# y = data["label"]

# # Scale features
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# # Train model
# model = RandomForestClassifier()
# model.fit(X_scaled, y)

# # Save model
# os.makedirs("models", exist_ok=True)
# with open("models/rf_model.pkl", "wb") as f:
#     pickle.dump(model, f)

# print("✅ Model saved as models/rf_model.pkl")

# # Test the saved model
# model = pickle.load(open("models/rf_model.pkl", "rb"))
# print(model.predict([[0.1, 0.2, 0.3, 150, 0.01, 0.02, 20]]))

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load your training data
df = pd.read_csv("training_data.csv")

# Separate features and labels
X = df.drop("label", axis=1)
y = df["label"]

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("📊 Evaluation:\n", classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, "models/rf_model.pkl")
print("✅ Model saved to models/rf_model.pkl")