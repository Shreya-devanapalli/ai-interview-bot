import { useRef, useState } from "react";
import axios from "axios";
import EyeContactTracker from "./EyeContactTracker";

export default function Recorder({ onResult }) {
  const recorderRef = useRef(null);
  const chunksRef = useRef([]);

  const [recording, setRecording] = useState(false);
  const [status, setStatus] = useState("idle"); 
  // idle | recording | analyzing

  const [eyeContactScore, setEyeContactScore] = useState(5);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true
      });

      recorderRef.current = new MediaRecorder(stream);
      chunksRef.current = [];

      recorderRef.current.ondataavailable = (e) => {
        chunksRef.current.push(e.data);
      };

      recorderRef.current.onstop = async () => {
        setStatus("analyzing");

        try {
          const blob = new Blob(chunksRef.current, {
            type: "audio/webm"
          });

          const formData = new FormData();
          formData.append("audio", blob);
          formData.append("eye_contact_score", eyeContactScore);

          const response = await axios.post(
            "http://127.0.0.1:8000/analyze",
            formData,
            { timeout: 45000 }
          );

          onResult(response.data);
        } catch (error) {
          console.error("Analysis failed:", error);
          alert("Analysis failed. Please try again.");
        } finally {
          setStatus("idle");
        }
      };

      recorderRef.current.start();
      setRecording(true);
      setStatus("recording");
    } catch (err) {
      console.error(err);
      alert("Microphone access denied.");
    }
  };

  const stopRecording = () => {
    if (!recorderRef.current) return;

    recorderRef.current.stop();

    // release microphone
    recorderRef.current.stream
      .getTracks()
      .forEach(track => track.stop());

    setRecording(false);
  };

  return (
    <div className="card">
      <h3>Answer Recording</h3>

      {/* Eye contact tracker runs ONLY while recording */}
      {recording && (
        <EyeContactTracker onScore={setEyeContactScore} />
      )}

      {status === "recording" && (
        <p style={{ color: "red", fontWeight: "bold" }}>
          🎙 Recording… Maintain eye contact
        </p>
      )}

      {status === "analyzing" && (
        <p style={{ color: "blue", fontWeight: "bold" }}>
          ⏳ Analyzing response…
        </p>
      )}

      {!recording ? (
        <button onClick={startRecording}>
          ▶ Start Recording
        </button>
      ) : (
        <button onClick={stopRecording}>
          ⏹ Stop Recording
        </button>
      )}
    </div>
  );
}


