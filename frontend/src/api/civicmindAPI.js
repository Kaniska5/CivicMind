// frontend/src/api/civicmindAPI.js

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function handleResponse(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Something went wrong. Please try again.");
  }
  return res.json();
}

export async function askPolicyPulse(question) {
  const res = await fetch(`${BASE_URL}/policy-pulse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return handleResponse(res);
}

export async function submitGrievance(issue) {
  const res = await fetch(`${BASE_URL}/grievance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ issue }),
  });
  return handleResponse(res);
}

export async function matchSchemes(profile) {
  const res = await fetch(`${BASE_URL}/scheme-match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  return handleResponse(res);
}
