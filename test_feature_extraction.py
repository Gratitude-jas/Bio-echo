from app.services.extract_features import extract_features
import os
import pandas as pd

cleaned_dir = "data/cleaned"
output_path = "data/features/features.csv"

features_list = []

for filename in os.listdir(cleaned_dir):
    if filename.endswith(".wav"):
        file_path = os.path.join(cleaned_dir, filename)
        features = extract_features(file_path)
        features["filename"] = filename
        features_list.append(features)

df = pd.DataFrame(features_list)
df.to_csv(output_path, index=False)
print(f"✅ Features saved to {output_path}")