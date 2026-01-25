export default function HistoryPanel() {
  const history = JSON.parse(localStorage.getItem("interviewHistory")) || [];

  if (!history.length) return null;

  return (
    <div className="card">
      <h3>Past Interviews</h3>
      <ul>
        {history.slice(0, 5).map((item, i) => (
          <li key={i}>
            {item.role} – Score: {item.score}/10
          </li>
        ))}
      </ul>
    </div>
  );
}
