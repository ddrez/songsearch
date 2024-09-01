# Search songs by lyrics

Ever wanted to find a song for which there are no lyrics? (like some EDM tracks with just a few repeated phrases)

This proof-of-concept is intented:
1) Extract vocals from audio files
2) Translate it into text
3) Create a searchable database


# Build

```
pip install -U uv
git clone https://github.com/ddrez/songsearch
cd songsearch
uv sync
source .venv/bin/activate
```

# Run

```
python -m songsearch index music/**/*.mp3
python -m songsearch search "some query"
```

# Thoughts

There was no any quantitave testing.

The vocal extraction step may include some sound effects in voice spectrum, that induce random tokens such as "Thanks for watching", "Bye" during STT step (see [whisper discussion](https://github.com/openai/whisper/discussions/1455)).
It may be corrected by additional preprocessing of the audio signal prior to STT or by fine-tuning voice extraction model.

During STT, language detection may fail (one can use explicit -l flag).

The search step and database backend are subject to change.

It takes about 5 minutes to process 1 song on a laptop CPU.


# Credits

[demucs](https://github.com/adefossez/demucs)
[faster_whisper](https://github.com/SYSTRAN/faster-whisper)
[metaphone](https://github.com/oubiwann/metaphone)
