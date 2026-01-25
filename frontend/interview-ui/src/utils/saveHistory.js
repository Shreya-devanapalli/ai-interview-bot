export function saveHistory(entry) {
  const history = JSON.parse(localStorage.getItem("interviewHistory")) || [];
  history.unshift(entry);
  localStorage.setItem("interviewHistory", JSON.stringify(history));
}
