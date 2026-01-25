import librosa
import numpy as np

def analyze_audio(audio_path):
    y, sr = librosa.load(audio_path)
    tempo = librosa.beat.tempo(y=y, sr=sr)[0]
    energy = float(np.mean(librosa.feature.rms(y=y)))
    return {
        "speaking_rate": round(float(tempo), 2),
        "energy": round(energy, 4)
    }

