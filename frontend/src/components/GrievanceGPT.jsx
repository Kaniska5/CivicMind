// frontend/src/components/GrievanceGPT.jsx
import { useState } from "react";
import { submitGrievance } from "../api/civicmindAPI";

export default function GrievanceGPT() {
  const [issue,   setIssue]   = useState("");
  const [result,  setResult]  = useState(null);
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState("");

  const handleSubmit = async () => {
    if (!issue.trim()) return;
    setLoading(true); setError(""); setResult(null);
    try {
      const data = await submitGrievance(issue);
      setResult(data);
    } catch (e) {
      console.error(e);
      setError(e.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="module-card">
      <h2>GrievanceGPT</h2>
      <p className="subtitle">Describe your problem and get department routing, document checklist, and a complaint letter.</p>
      <textarea
        value={issue}
        onChange={e => setIssue(e.target.value)}
        placeholder="e.g. My ration card application was rejected 3 months ago and I haven't received any response."
        rows={4}
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? <span className="spinner" /> : "Submit Grievance"}
      </button>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="response">
          <div><strong>Department:</strong><p>{result.department}</p></div>
          <div><strong>Documents Required:</strong><p style={{ whiteSpace: "pre-line" }}>{result.documents_required}</p></div>
          <div><strong>Complaint Letter:</strong><p style={{ whiteSpace: "pre-line" }}>{result.complaint_letter}</p></div>
          <div><strong>Next Steps:</strong><p style={{ whiteSpace: "pre-line" }}>{result.next_steps}</p></div>
        </div>
      )}
    </div>
  );
}
