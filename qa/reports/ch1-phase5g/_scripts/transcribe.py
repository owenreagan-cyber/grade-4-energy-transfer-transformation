#!/usr/bin/env python3
"""Transcribe candidate videos via faster-whisper (base.en, cpu int8).

Bypasses PyAV: decode each video to 16 kHz mono WAV with ffmpeg, read the WAV as float32
numpy, and pass the array directly to model.transcribe (skips decode_audio / av.open).
Writes one .txt transcript per video.
"""
import subprocess, sys, os, wave, tempfile
import numpy as np
from faster_whisper import WhisperModel


def wav_to_float32(path):
    with wave.open(path, "rb") as w:
        n = w.getnframes()
        data = w.readframes(n)
        arr = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        if w.getnchannels() > 1:
            arr = arr.reshape(-1, w.getnchannels()).mean(axis=1)
    return arr


def main():
    outdir = sys.argv[1]
    paths = sys.argv[2:]
    os.makedirs(outdir, exist_ok=True)
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    for p in paths:
        name = os.path.basename(p)
        out = os.path.join(outdir, name + ".txt")
        if os.path.exists(out):
            print("SKIP", name); continue
        wav = os.path.join(tempfile.mkdtemp(), "a.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", "16000", wav],
                       check=True)
        audio = wav_to_float32(wav)
        segments, info = model.transcribe(audio, beam_size=5, language="en", vad_filter=True)
        lines = []
        for seg in segments:
            lines.append("[%06.1f-%06.1f] %s" % (seg.start, seg.end, seg.text.strip()))
        with open(out, "w") as f:
            f.write("\n".join(lines) + "\n")
        print("DONE", name, "segments:", len(lines))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
