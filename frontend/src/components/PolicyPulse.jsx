// frontend/src/components/PolicyPulse.jsx
import { useState } from "react";
import { askPolicyPulse } from "../api/civicmindAPI";

export default function PolicyPulse() {
  const [question, setQuestion] = useState("");
  const [answer,   setAnswer]   = useState("");
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState("");

  const handleSubmit = async () => {
    if (!question.trim()) return;
    setLoading(true); setError(""); setAnswer("");
    try {
      const data = await askPolicyPulse(question);
      setAnswer(data.answer);
    } catch (e) {
      console.error(e);
      setError(e.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="module-card">
      <h2>PolicyPulse</h2>
      <p className="subtitle">Ask about government schemes, RTI, CPGRAMS, or budget announcements.</p>
      <textarea
        value={question}
        onChange={e => setQuestion(e.target.value)}
        placeholder="e.g. What is PM-KISAN? Am I eligible for Ayushman Bharat?"
        rows={4}
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? <span className="spinner" /> : "Ask"}
      </button>
      {error  && <div className="error">{error}</div>}
      {answer && <div className="response"><strong>Answer:</strong><p>{answer}</p></div>}
    </div>
  );
}
