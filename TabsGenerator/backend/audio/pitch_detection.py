import librosa
import numpy as np

def extract_pitch(audio, sr, confidence_threshold=0.25):
    """
    Extract pitch and suppress low-confidence frames.
    """

    pitches, voiced_flag, voiced_probs = librosa.pyin(
        audio,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7"),
        sr=sr
    )

    # 🔥 Kill low-confidence pitch frames
    pitches[voiced_probs < confidence_threshold] = np.nan

    times = librosa.times_like(pitches, sr=sr)
    return times, pitches
