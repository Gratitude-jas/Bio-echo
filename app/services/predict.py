import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def train_model(features_csv, model_path="app/models/rf_model.pkl"):
    df = pd.read_csv(features_csv)

    # Drop rows with NaNs
    df = df.dropna()

    # Assume filename format indicates label: 'P_' = Parkinson's, 'H_' = Healthy
    df["label"] = df["filename"].apply(lambda x: 1 if x.startswith("P_") else 0)

    X = df.drop(columns=["filename", "label"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

    return report

def predict_sample(feature_dict, model_path="app/models/rf_model.pkl"):
    model = joblib.load(model_path)
    df = pd.DataFrame([feature_dict])
    prediction = model.predict(df)[0]
    return "Parkinson's" if prediction == 1 else "Healthy"