import { useEffect, useState } from "react";
import axios from "axios";

export default function HistoryPanel() {

  const [history, setHistory] = useState([]);

  useEffect(() => {

    async function loadHistory() {

      try {

        const response = await axios.get(
          "http://127.0.0.1:8000/interviews"
        );

        setHistory(response.data);

      } catch (err) {
        console.error(err);
      }

    }

    loadHistory();

  }, []);

  if (!history.length) return null;

  return (
    <div className="card">
      <h3>Past Interviews</h3>

      <ul>

        {history.slice(0, 5).map((item) => (

          <li key={item.id}>

            <strong>{item.job_role}</strong>

            {" — Score: "}

            {item.score ?? "-"}/10

          </li>

        ))}

      </ul>

    </div>
  );
}