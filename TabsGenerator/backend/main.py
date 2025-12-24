# =========================
# AUDIO PIPELINE
# =========================
from backend.audio.preprocess import load_audio
from backend.audio.pitch_detection import extract_pitch
from backend.audio.time_bucket_smoothing import time_bucket_smoothing
from backend.audio.vocal_separation import separate_vocals

# =========================
# MUSIC PIPELINE
# =========================
from backend.music.freq_to_note import pitches_to_note
from backend.music.note_consolidation import (
    consolidate_notes,
    remove_short_notes,
    merge_adjacent_notes
)
from backend.music.note_to_fret import note_to_fret
from backend.music.tab_generator import generate_tab_events, build_ascii_tab
from backend.music.tab_formatter import wrap_ascii_tabs


def generate_tabs_from_song(audio_path, step=0.05):
    """
    Full pipeline:
    audio -> vocals -> pitch -> notes -> frets -> ASCII tabs
    """

    print("🎧 Separating vocals...")
    vocals_path = separate_vocals(audio_path)

    print("📥 Loading vocal audio...")
    audio, sr = load_audio(vocals_path)
    audio = audio / max(abs(audio))  # normalize

    print("🎵 Extracting pitch...")
    times, pitches = extract_pitch(audio, sr)

    print("⏱️ Smoothing time buckets...")
    bucket_times, bucket_pitches = time_bucket_smoothing(
        times, pitches, step=step
    )

    print("🎼 Converting pitch → notes...")
    notes = pitches_to_note(bucket_pitches)

    print("🧠 Consolidating notes...")
    events = consolidate_notes(notes, bucket_times)
    events = remove_short_notes(events, min_duration=0.15)
    events = merge_adjacent_notes(events, max_gap=0.2)

    print("🎸 Mapping notes → frets...")
    enriched_events = []
    skipped = 0
    for e in events:
        result = note_to_fret(e["note"])
        if result is None:
            skipped+=1
            continue

        string, fret = result
        e["string"] = string
        e["fret"] = fret
        enriched_events.append(e)

    events = enriched_events
    print(f"Skipped {skipped} notes due to fret mapping")
    print("📐 Generating tab columns...")
    tab_events = generate_tab_events(events, step=step)
    total_cols = max(e["end_col"] for e in tab_events) + 5

    print("📝 Building ASCII tabs...")
    ascii_tabs = build_ascii_tab(tab_events, total_cols)

    return ascii_tabs


# =========================
# RUN DIRECTLY
# =========================
if __name__ == "__main__":
    tabs = generate_tabs_from_song("backend/uploads/test_song.mp3")

    wrapped_tabs = wrap_ascii_tabs(tabs, width=70)

    print("\n🎸 PLAYABLE TABS:\n")

    for block in wrapped_tabs:
        for line in block:
            print(line)
        print()
