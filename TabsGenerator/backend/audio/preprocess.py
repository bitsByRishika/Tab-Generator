import librosa

def load_audio(file_path, target_sr = 16000):
    """
    Load an audio file, convert to mono, and resample.

    Parameters:
        file_path (str): path to audio file
        target_sr (int): target sampling rate (default 16kHz)

    Returns:
        audio (np.ndarray): mono audio waveform
        sr (int): sampling rate 
    """
    audio, sr = librosa.load(
        file_path,
        sr = target_sr,
        mono = True
    )
    audio = audio / max(abs(audio))
    return audio, sr