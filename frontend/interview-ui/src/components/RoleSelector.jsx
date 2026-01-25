export default function RoleSelector({ role, setRole }) {
  return (
    <div className="card">
      <h3>Select Interview Role</h3>
      <select value={role} onChange={e => setRole(e.target.value)}>
        <option value="HR">HR</option>
        <option value="TECH">Technical</option>
        <option value="MANAGERIAL">Managerial</option>
      </select>
    </div>
  );
}
