// frontend/src/components/SchemeMatch.jsx
import { useState } from "react";
import { matchSchemes } from "../api/civicmindAPI";

export default function SchemeMatch() {
  const [profile, setProfile] = useState({
    age: "",
    gender: "",
    annual_income: "",
    caste_category: "",
    state: "",
    occupation: "",
  });
  const [result,  setResult]  = useState("");
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState("");

  const handleChange = (e) =>
    setProfile({ ...profile, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    setLoading(true); setError(""); setResult("");
    try {
      const payload = {
        ...profile,
        age: parseInt(profile.age),
        annual_income: parseFloat(profile.annual_income),
      };
      const data = await matchSchemes(payload);
      setResult(data.schemes);
    } catch (e) {
      console.error(e);
      setError(e.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const fields = [
    { name: "age",            label: "Age",               type: "number", placeholder: "e.g. 35" },
    { name: "gender",         label: "Gender",            type: "text",   placeholder: "Male / Female / Other" },
    { name: "annual_income",  label: "Annual Income (₹)", type: "number", placeholder: "e.g. 80000" },
    { name: "caste_category", label: "Caste Category",    type: "text",   placeholder: "General / OBC / SC / ST" },
    { name: "state",          label: "State",             type: "text",   placeholder: "e.g. Tamil Nadu" },
    { name: "occupation",     label: "Occupation",        type: "text",   placeholder: "e.g. Farmer / Daily Wage Worker" },
  ];

  return (
    <div className="module-card">
      <h2>SchemeMatch AI</h2>
      <p className="subtitle">Enter your profile and get a list of every welfare scheme you are eligible for.</p>
      <div className="form-grid">
        {fields.map((f) => (
          <div key={f.name} className="form-field">
            <label>{f.label}</label>
            <input
              type={f.type}
              name={f.name}
              value={profile[f.name]}
              onChange={handleChange}
              placeholder={f.placeholder}
            />
          </div>
        ))}
      </div>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? <span className="spinner" /> : "Find My Schemes"}
      </button>
      {error  && <div className="error">{error}</div>}
      {result && (
        <div className="response">
          <strong>Eligible Schemes:</strong>
          <p style={{ whiteSpace: "pre-line" }}>{result}</p>
        </div>
      )}
    </div>
  );
}
