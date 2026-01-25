import { generatePDF } from "../utils/generatePDF";
import ConfidenceBar from "./ConfidenceBar";

export default function Feedback({ data }) {
  return (
    <div className="card fade-in">
      <h2>Interview Result</h2>

      <ConfidenceBar score={data.score} />

      <p><strong>Transcription:</strong></p>
      <p>{data.transcript}</p>

      <ul>
        {data.feedback.map((f, i) => <li key={i}>{f}</li>)}
      </ul>

      <button onClick={() => generatePDF(data)}>
        📄 Download Feedback PDF
      </button>
    </div>
  );
}

