import subprocess
from pathlib import Path

def convert_webm_to_wav(webm_path: Path) -> Path:
    wav_path = webm_path.with_suffix(".wav")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", str(webm_path),
            "-ac", "1",
            "-ar", "16000",
            str(wav_path)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    return wav_path

