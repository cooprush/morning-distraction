"""Turn ChatGPT's prepared daily script into audio. No LLM API required."""
import datetime as dt
import os
import subprocess
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
TODAY = dt.datetime.now(ZoneInfo("Europe/London")).strftime("%Y-%m-%d")
INPUT = ROOT / "episodes" / f"{TODAY}.txt"


def run(args, timeout=2400):
    subprocess.run(args, check=True, timeout=timeout)


def audio_seconds(path):
    return float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip())


def main():
    if not INPUT.is_file():
        raise RuntimeError(
            f"ChatGPT has not supplied today's script ({INPUT}). "
            "No old script or invented episode will be published."
        )
    content = INPUT.read_text(encoding="utf-8").strip()
    words = len(content.split())
    if not 3600 <= words <= 5400:
        raise RuntimeError(f"Unexpected script length: {words} words. Expected 3600–5400.")

    OUT.mkdir(exist_ok=True)
    wav = OUT / f"morning-{TODAY}.wav"
    mp3 = OUT / f"morning-{TODAY}.mp3"

    run([
        "python", "-m", "piper",
        "--model", "en_GB-cori-medium",
        "--data-dir", "voices",
        "--input-file", str(INPUT),
        "-f", str(wav),
    ])
    run([
        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(wav), "-codec:a", "libmp3lame", "-b:a", "64k", str(mp3)
    ], timeout=360)
    duration = audio_seconds(mp3)
    if duration < 25 * 60:
        raise RuntimeError(
            f"Audio only {duration/60:.1f} minutes. "
            "Not publishing a shorter recording as a 30-minute podcast."
        )
    (OUT / "release-notes.md").write_text(
        f"The Morning Distraction for {TODAY}.\n\n"
        f"DurationSeconds: {int(duration)}\n"
        "Original British audio comedy, curiosity and satire. "
        "Script by ChatGPT; synthetic voice by Piper.\n",
        encoding="utf-8"
    )
    print(f"Prepared {mp3} from {words} words, {duration/60:.1f} minutes", flush=True)


if __name__ == "__main__":
    main()
