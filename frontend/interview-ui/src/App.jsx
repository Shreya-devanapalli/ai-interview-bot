import { useState } from "react";
import { QUESTIONS } from "./data/questions";
import Recorder from "./components/Recorder";
import QuestionCard from "./components/QuestionCard";
import Feedback from "./components/Feedback";
import RoleSelector from "./components/RoleSelector";
import HistoryPanel from "./components/HistoryPanel";
import { saveHistory } from "./utils/saveHistory";

function App() {
  const [role, setRole] = useState("HR");
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);

  const generateQuestion = () => {
    const list = QUESTIONS[role];
    setQuestion(list[Math.floor(Math.random() * list.length)]);
    setResult(null);
  };

  const handleResult = (data) => {
    setResult(data);
    saveHistory({ role, score: data.score });
  };

  return (
    <div className="container">
      <h1 className="title">AI Interview Simulator</h1>

      <RoleSelector role={role} setRole={setRole} />
      <button onClick={generateQuestion}>Generate Question</button>

      {question && <QuestionCard question={question} />}
      {question && <Recorder onResult={handleResult} />}
      {result && <Feedback data={result} />}

      <HistoryPanel />
    </div>
  );
}

export default App;

