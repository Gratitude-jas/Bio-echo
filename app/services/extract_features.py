import librosa
import numpy as np

def extract_features(audio_path, target_sr=16000):
    y, sr = librosa.load(audio_path, sr=target_sr)

    if y is None or len(y)<1000:
        raise ValueError("Audio too short or unreadable.")

    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfccs, axis=1) if mfccs.shape[1] > 0 else np.zeros(13)

    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[magnitudes > np.median(magnitudes)]
    pitch_mean = np.mean(pitch_values) if len(pitch_values) > 0 else 0
    pitch_std = np.std(pitch_values) if len(pitch_values) > 0 else 0
    jitter = pitch_std / pitch_mean if pitch_mean != 0 else 0

    shimmer = np.std(y)

    try:
        S, phase = librosa.magphase(librosa.stft(y))
        harmonic = np.mean(S[phase > 0]) if np.any(phase > 0) else 0
        noise = np.mean(S[phase == 0]) if np.any(phase == 0) else 1e-6
        hnr = 10 * np.log10(harmonic / noise) if noise != 0 else 0
    except:
        hnr = 0

    return {
        "mfcc_1": float(mfcc_mean[0]),
        "mfcc_2": float(mfcc_mean[1]),
        "mfcc_3": float(mfcc_mean[2]),
        "pitch": float(pitch_mean),
        "jitter": float(jitter),
        "shimmer": float(shimmer),
        "hnr": float(hnr)
    }

    # Build feature dict
    features = {f"mfcc_{i+1}": float(mfcc_mean[i]) for i in range(13)}
    features.update({
        "pitch": float(pitch_mean),
        "jitter": float(jitter),
        "shimmer": float(shimmer),
        "hnr": float(hnr)
    })

    # Replace NaNs or infs with 0
    for k, v in features.items():
        if np.isnan(v) or np.isinf(v):
            features[k] = 0.0

    return features
