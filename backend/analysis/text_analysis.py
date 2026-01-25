from textblob import TextBlob

def analyze_text(text):
    blob = TextBlob(text)
    return {
        "word_count": len(text.split()),
        "sentiment": round(blob.sentiment.polarity, 2),
        "subjectivity": round(blob.sentiment.subjectivity, 2)
    }

