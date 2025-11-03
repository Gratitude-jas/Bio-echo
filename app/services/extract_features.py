import librosa
import numpy as np

def extract_features(audio_path, target_sr=16000):
    y, sr = librosa.load(audio_path, sr=target_sr)

    # MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfccs, axis=1)

    # Pitch (F0)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[magnitudes > np.median(magnitudes)]
    pitch_mean = np.mean(pitch_values) if len(pitch_values) > 0 else 0
    pitch_std = np.std(pitch_values) if len(pitch_values) > 0 else 0
    jitter = pitch_std / pitch_mean if pitch_mean != 0 else 0

    # Shimmer (approximate via amplitude variation)
    shimmer = np.std(y)

    # HNR (harmonics-to-noise ratio)
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