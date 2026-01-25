export default function ConfidenceBar({ score }) {
  const width = Math.min(score * 10, 100);

  return (
    <div className="card">
      <h3>Confidence Level</h3>
      <div className="bar-bg">
        <div
          className="bar-fill"
          style={{ width: `${width}%` }}
        />
      </div>
      <p>{score}/10</p>
    </div>
  );
}
