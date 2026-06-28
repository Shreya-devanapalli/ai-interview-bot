from pathlib import Path

from analysis.speech_to_text import transcribe_audio
from analysis.text_analysis import analyze_text
from analysis.audio_analysis import analyze_audio
from feedback.feedback_generator import generate_feedback
from utils.convert_audio import convert_webm_to_wav


def run_analysis(audio_path: Path, eye_contact_score: int):

    wav_path = convert_webm_to_wav(audio_path)

    transcript = transcribe_audio(str(wav_path))

    text_result = analyze_text(transcript)

    audio_result = analyze_audio(str(wav_path))

    video_result = {
        "eye_contact_score": eye_contact_score
    }

    feedback_data = generate_feedback(
        text_result,
        audio_result,
        video_result
    )

    return {
        "transcript": transcript,
        "analysis": {
            "text": text_result,
            "audio": audio_result,
            "video": video_result
        },
        "feedback": feedback_data["remarks"],
        "score": feedback_data["score"]
    }