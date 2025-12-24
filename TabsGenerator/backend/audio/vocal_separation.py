import subprocess
from pathlib import Path


def separate_vocals(audio_path, output_dir="backend/audio/separated"):
    """
    Run Demucs to separate vocals.
    Uses cached vocals if already present.
    """

    audio_path = Path(audio_path)
    output_dir = Path(output_dir)

    song_name = audio_path.stem

    # ✅ DEFINE vocals_path FIRST
    vocals_path = (
        output_dir / "htdemucs" / song_name / "vocals.wav"
    )

    # ✅ NOW it is safe to check
    if vocals_path.exists():
        print("🎵 Using cached vocals")
        return str(vocals_path)

    print("🎧 Running Demucs (this may take time)...")

    command = [
        "python",
        "-m",
        "demucs",
        str(audio_path),
        "-o",
        str(output_dir)
    ]

    subprocess.run(command, check=True)

    return str(vocals_path)
