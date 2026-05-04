import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.rag.rag_pipeline import RAGPipeline
from backend.services.civic_service import (
    handle_policy_query,
    handle_grievance,
    handle_scheme_match,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initialising RAGPipeline...")
    app.state.pipeline = RAGPipeline()
    logger.info("RAGPipeline ready")
    yield
    logger.info("Shutting down")


app = FastAPI(lifespan=lifespan)

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request models ──────────────────────────────────────────

class PolicyRequest(BaseModel):
    question: str


class GrievanceRequest(BaseModel):
    issue: str


class SchemeRequest(BaseModel):
    age: int
    gender: str
    annual_income: float
    caste_category: str
    state: str
    occupation: str


# ── Endpoints ───────────────────────────────────────────────

@app.post("/policy-pulse")
async def policy_pulse(req: PolicyRequest, request: Request):
    pipeline = request.app.state.pipeline
    return handle_policy_query(pipeline, req.question)


@app.post("/grievance")
async def grievance(req: GrievanceRequest, request: Request):
    pipeline = request.app.state.pipeline
    return handle_grievance(pipeline, req.issue)


@app.post("/scheme-match")
async def scheme_match(req: SchemeRequest, request: Request):
    pipeline = request.app.state.pipeline
    profile = {
        "age": req.age,
        "gender": req.gender,
        "annual_income": req.annual_income,
        "caste_category": req.caste_category,
        "state": req.state,
        "occupation": req.occupation,
    }
    return handle_scheme_match(pipeline, profile)
