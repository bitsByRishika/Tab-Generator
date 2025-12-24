import numpy as np
from scipy import stats
import librosa

def time_bucket_smoothing(times, pitches, step=0.1):

    start_time = times[0]
    end_time = times[-1]

    bucket_times = []
    bucket_pitches = []

    t = start_time
    while t < end_time:
        idx = np.where((times >= t) & (times < t + step))[0]

        if len(idx) == 0:
            bucket_pitches.append(np.nan)
        else:
            values = pitches[idx]
            values = values[~np.isnan(values)]

            if len(values) == 0:
                bucket_pitches.append(np.nan)
            else:
                # 1. Convert Hz to MIDI integers to group similar frequencies
                midi_values = librosa.hz_to_midi(values).round().astype(int)
                
                # 2. Find the Mode (most frequent MIDI note)
                mode_result = stats.mode(midi_values, keepdims=True)
                dominant_midi = mode_result.mode[0]
                
                # 3. Convert back to a stable Frequency (Hz)
                bucket_pitches.append(librosa.midi_to_hz(dominant_midi))

        bucket_times.append(t + step / 2)
        t += step

    return bucket_times, bucket_pitches
