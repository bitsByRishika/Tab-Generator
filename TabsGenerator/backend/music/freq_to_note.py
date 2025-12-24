import numpy as np
import librosa

def hz_safe_note(pitch_hz):
    if pitch_hz is None or np.isnan(pitch_hz):
        return None
    
    midi = librosa.hz_to_midi(pitch_hz)
    rounded_midi = int(np.round(midi))
    note = librosa.midi_to_note(rounded_midi)

    return note

def pitches_to_note(pitches):
    notes=[]
    for p in pitches:
        notes.append(hz_safe_note(p))

    return notes