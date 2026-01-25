export default function QuestionCard({ question }) {
  return (
    <div style={{ marginTop: 20 }}>
      <h2>❓ Interview Question</h2>
      <p>{question}</p>
    </div>
  );
}
