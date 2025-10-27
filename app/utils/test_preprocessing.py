import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.preprocess import preprocess_audio

raw_dir = "data/raw"
cleaned_dir = "data/cleaned"

for filename in os.listdir(raw_dir):
    if filename.endswith(".wav"):
        input_path = os.path.join(raw_dir, filename)
        output_path = os.path.join(cleaned_dir, filename)

        try:
            preprocess_audio(input_path, output_path)
            print(f"✅ Preprocessed: {filename}")
        except Exception as e:
            print(f"❌ Failed: {filename} — {e}")