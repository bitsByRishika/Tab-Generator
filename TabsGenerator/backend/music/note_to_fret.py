import librosa

STRING_TUNING={
    6 : 'E2',
    5 : 'A2',
    4 : 'D3',
    3 : 'G3',
    2 : 'B3',
    1 : 'E4',
}

def note_to_fret(note):
    """
    Map note to guitar fret with vocal-melody logic:
    - Prefer high strings (1,2,3)
    - Keep frets between 0–15
    - Auto octave-shift if needed
    """

    target_midi = librosa.note_to_midi(note)

    # Preferred strings for vocal melodies
    preferred_order = [1, 2, 3, 4, 5, 6]

    # Try octave shifts (0, -12, +12)
    for octave_shift in [0, -12, 12]:
        shifted_midi = target_midi + octave_shift

        for string in preferred_order:
            open_midi = librosa.note_to_midi(STRING_TUNING[string])
            fret = shifted_midi - open_midi

            # Guitar-vocal sweet spot
            if 0 <= fret <= 15:
                return (string, fret)

    return None
