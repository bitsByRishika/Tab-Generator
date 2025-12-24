import librosa
from collections import Counter
import numpy as np

def same_note(note1, note2, tolerance=1):
    """
    Check if two notes are musically the same within a semitone tolerance.
    """
    if note1 is None or note2 is None:
        return False

    midi1 = librosa.note_to_midi(note1)
    midi2 = librosa.note_to_midi(note2)

    return abs(midi1 - midi2) <= tolerance

def consolidate_notes(notes, times, window_size=5, tolerance=1):
    """
    Consolidate fluctuating notes into sustained musical notes.
    """
    # --- START OF SMOOTHING PASS ---
    # This removes 'flicker' where a single frame might jump to a wrong note
    smoothed_notes = []
    for i in range(len(notes)):
        # Look at a small local window (2 frames back, 2 frames forward)
        window = notes[max(0, i-2):min(len(notes), i+3)]
        valid_window = [n for n in window if n is not None]
        
        if valid_window:
            # Reassign the current note to the most common note in its neighborhood
            smoothed_notes.append(Counter(valid_window).most_common(1)[0][0])
        else:
            smoothed_notes.append(None)
    
    # Replace the original notes with our cleaned version
    notes = smoothed_notes
    # --- END OF SMOOTHING PASS ---

    events = []
    i = 0
    n = len(notes)

    while i < n:
        # Skip rests (None values)
        if notes[i] is None:
            i += 1
            continue

        start_time = times[i]
        window_notes = []
        j = i

        # Collect a small window of notes to determine the dominant pitch
        while j < n and len(window_notes) < window_size:
            if notes[j] is not None:
                window_notes.append(notes[j])
            j += 1

        if not window_notes:
            i += 1
            continue

        # Find dominant note
        dominant_note = Counter(window_notes).most_common(1)[0][0]

        # Extend note until a real change happens (outside of tolerance)
        k = j
        while k < n:
            if notes[k] is None:
                # If we hit a short silence, keep checking a bit further
                k += 1
                continue
            if not same_note(notes[k], dominant_note, tolerance):
                break
            k += 1

        # Calculate end time based on the last valid frame of this note
        end_time = times[k - 1]

        events.append({
            "note": dominant_note,
            "start": start_time,
            "end": end_time
        })

        i = k
    
    return events

def remove_short_notes(events, min_duration=0.25):
    """
    Remove notes shorter than min_duration seconds.
    Guitar-realistic minimum hold time.
    """
    cleaned = []    

    for e in events:
        duration = e["end"] - e["start"]
        if duration >= min_duration:
            cleaned.append(e)

    return cleaned

def merge_adjacent_notes(events, max_gap=0.2):
    """
    Merge same notes if the gap between them is small.
    """
    if not events:
        return []

    merged = [events[0]]

    for e in events[1:]:
        last = merged[-1]

        # If it's the same note and the 'silence' between them is tiny, merge them
        if (
            e["note"] == last["note"]
            and (e["start"] - last["end"]) <= max_gap
        ):
            last["end"] = e["end"]
        else:
            merged.append(e)

    return merged