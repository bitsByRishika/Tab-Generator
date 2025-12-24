🎸 TabsGenerator

Generate guitar tabs for vocal melodies directly from an uploaded song.
This project focuses on extracting the lead vocal line and converting it into playable guitar tabs, similar to how guitarists play vocals as a melodic substitute.

⚠️ This is an experimental / research-style project.
Output is not expected to be perfect and is designed to improve iteratively with musical tuning.

✨ Features

🎧 Upload any song (.mp3)

🗣️ Separate vocals from the mix using Demucs
🎵 Extract vocal pitch (fundamental frequency) using librosa.pyin
🧠 Consolidate pitch into musical notes (ignores jitter & noise)
🎸 Map notes to guitar strings and frets
📐 Generate ASCII guitar tabs
📝 Tabs are rendered in playable rows, not raw timelines

