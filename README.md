🎤 AI Interview Simulator

An AI-powered interview practice platform that evaluates a candidate’s confidence, communication quality, and eye contact using audio analysis, speech transcription, and real-time webcam signals.

This project is designed to simulate real interview conditions and provide actionable feedback to help users improve their performance.

🚀 Features

🎙 Audio Recording & Transcription

Records interview answers via microphone

Uses OpenAI Whisper for accurate speech-to-text transcription

🧠 Communication Analysis

Text analysis (length, clarity)

Audio confidence analysis (energy, speaking intensity)

👀 Eye Contact & Confidence Estimation

Lightweight frontend-based webcam analysis

Estimates eye contact consistency during response

Avoids heavy backend video processing for performance

📊 Final Interview Score (0–10)

Combines text quality, audio confidence, and eye contact

Simple, interpretable scoring system

📄 Downloadable Feedback Report

Generates a PDF report with:

Score

Transcription

Feedback points

🧾 Interview History

Saves previous interview scores locally for future reference

🎨 Modern Web UI

Clean layout

Animations & progress indicators

Role-based interview questions (HR / Technical / Managerial)

🛠️ Tech Stack
Frontend

 React (Vite)

 MediaRecorder API

 MediaPipe (Face Detection)

 Axios

 jsPDF (PDF report generation)

 CSS animations

Backend

 FastAPI

 OpenAI Whisper

 FFmpeg

 librosa

 Python 3.11


⚙️ Installation & Setup
1️. Clone the repository
git clone https://github.com/Shreya-devanapalli/ai-interview-bot.git
cd ai-interview-bot

2️. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Start backend:
uvicorn main:app --reload

3️. Frontend Setup
cd frontend/interview-ui
npm install
npm run dev

🧑‍💻 Author

Developed by Shreya Devanapalli
Data Science Enthusiast | Machine Learning

📫 LinkedIn Profile : www.linkedin.com/in/shreya-devanapalli

📂 GitHub Portfolio : https://github.com/Shreya-devanapalli