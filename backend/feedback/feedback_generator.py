def generate_feedback(text, audio, video):
    feedback = []

    if text["word_count"] < 40:
        feedback.append("Try giving more detailed answers with examples.")

    if audio["energy"] < 0.01:
        feedback.append("Speak with more confidence and clarity.")

    feedback.append(
        "Eye contact score is estimated. Real-time video analysis can be enabled asynchronously."
    )

    score = 0
    score += min(text["word_count"] / 10, 4)
    score += min(audio["energy"] * 500, 3)
    score += 2  # baseline for eye contact

    return {
        "score": round(score, 1),
        "remarks": feedback or ["Good overall response."]
    }



