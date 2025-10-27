import librosa
import soundfile as sf
import os

def preprocess_audio(input_path, output_path, target_sr=16000):
    y, sr = librosa.load(input_path, sr=None)

    # Trim silence
    y_trimmed, _ = librosa.effects.trim(y)

    # Normalize volume
    y_normalized = y_trimmed / max(abs(y_trimmed))

    # Resample to target sample rate
    y_resampled = librosa.resample(y_normalized, orig_sr=sr, target_sr=target_sr)

    # Save cleaned audio
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, y_resampled, target_sr)

    return output_path