# CivicMind — RAG-Powered Civic Intelligence Platform

---

## What is CivicMind?

CivicMind is a three-module AI platform built on Retrieval-Augmented Generation (RAG)
that connects Indian citizens to welfare information in plain language.

| Module             | What it does                                                                  |
| ------------------ | ----------------------------------------------------------------------------- |
| **PolicyPulse**    | Answers questions about 50+ government schemes, RTI Act, CPGRAMS, budget      |
| **GrievanceGPT**   | Routes complaints, lists required documents, auto-generates complaint letters |
| **SchemeMatch AI** | Matches a citizen profile to every eligible welfare scheme                    |

---

## Project Structure

```
CivicMind/
├── backend/
│   ├── main.py                  # FastAPI app with lifespan-managed pipeline
│   ├── ingest.py                # Document ingestion + FAISS index builder
│   ├── rag/
│   │   └── rag_pipeline.py      # RAG pipeline (embeddings, LLM, retrieval)
│   ├── services/
│   │   └── civic_service.py     # Business logic + input validation
│   └── data/
│       └── vector_store/        # Persisted FAISS index (auto-generated)
├── knowledge_base/
│   ├── central_schemes/         # Government scheme PDFs
│   ├── legal_docs/              # RTI Act, CPGRAMS TXT files
│   ├── state_docs/              # State-level policy PDFs
│   └── budget/                  # Budget announcement TXTs
├── frontend/
│   └── src/
│       ├── components/          # PolicyPulse, GrievanceGPT, SchemeMatch
│       └── api/
│           └── civicmindAPI.js  # Centralised API layer
├── .env.example
└── requirements.txt
```

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Groq API key from [console.groq.com](https://console.groq.com)

---

### Step 1 — Clone and configure

```bash
git clone https://github.com/Kaniska5/CivicMind.git
cd CivicMind
```

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
ALLOWED_ORIGINS=http://localhost:5173
```

Create a `frontend/.env` file:

```
VITE_API_URL=http://localhost:8000
```

---

### Step 2 — Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3 — Add knowledge base documents

Drop your PDF or TXT files into the appropriate folders:

```
knowledge_base/central_schemes/   ← government scheme PDFs
knowledge_base/legal_docs/        ← RTI Act, CPGRAMS TXT files
knowledge_base/state_docs/        ← state-level policy PDFs
knowledge_base/budget/            ← budget announcement TXTs
```

Sample files are already included to test with.

---

### Step 4 — Run ingestion (build FAISS index)

```bash
python -m backend.ingest
```

You should see:

```
INFO - Loaded: pm_kisan.txt
INFO - Total documents loaded: 8
INFO - Total chunks created: 42
INFO - FAISS index saved to: backend/data/vector_store
```

---

### Step 5 — Start the backend

```bash
uvicorn backend.main:app --reload --port 8000
```

API will be live at: [http://localhost:8000](http://localhost:8000)  
Swagger docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Step 6 — Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend at: [http://localhost:5173](http://localhost:5173)

---

## API Reference

### POST /policy-pulse

```json
{ "question": "What is PM-KISAN and how do I apply?" }
```

### POST /grievance

```json
{
  "issue": "My ration card application was rejected 3 months ago and I have received no response."
}
```

### POST /scheme-match

```json
{
  "age": 35,
  "gender": "Female",
  "annual_income": 80000,
  "caste_category": "SC",
  "state": "Tamil Nadu",
  "occupation": "Farmer"
}
```

---

## Example Queries to Test

**PolicyPulse:**

- "What is Ayushman Bharat and who is eligible?"
- "How do I file an RTI application?"
- "What are the benefits of PM Ujjwala Yojana?"

**GrievanceGPT:**

- "My electricity connection was cut without notice 2 weeks ago"
- "I applied for a caste certificate 6 months ago and got no response"

**SchemeMatch AI:**

- Profile: Age 28, Female, Income ₹60,000, OBC, Tamil Nadu, Farmer

---

## Tech Stack

| Layer           | Technology                                      |
| --------------- | ----------------------------------------------- |
| Frontend        | React.js (Vite) + CSS                           |
| API             | FastAPI (Python)                                |
| RAG Chain       | LangChain                                       |
| Vector Store    | FAISS (local)                                   |
| Embedding Model | HuggingFace `all-MiniLM-L6-v2` via LangChain   |
| LLM             | Groq LLaMA 3.1 8B Instant via LangChain         |

---

## Architecture

The backend follows a layered architecture:

```
Request → FastAPI Controller (main.py)
              ↓
          Service Layer (civic_service.py)   ← validation + business logic
              ↓
          RAG Pipeline (rag_pipeline.py)     ← embeddings, retrieval, LLM chaining
              ↓
          FAISS Vector Store                 ← local knowledge base index
```

GrievanceGPT uses multi-step LLM chaining — department identification, document retrieval, complaint letter generation, and next-steps guidance are handled as separate chained calls rather than a single prompt.

---

## Contributors

- [haritha2k5](https://github.com/haritha2k5)
- [Kaniska5](https://github.com/Kaniska5)
