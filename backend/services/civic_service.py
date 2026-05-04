import logging
from fastapi import HTTPException
from backend.rag.rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)


def handle_policy_query(pipeline: RAGPipeline, question: str) -> dict:
    question = question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Question cannot be empty")
    try:
        answer = pipeline.query_policy(question)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Policy query error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process policy query")


def handle_grievance(pipeline: RAGPipeline, issue: str) -> dict:
    issue = issue.strip()
    if len(issue) < 10:
        raise HTTPException(
            status_code=422,
            detail="Please describe your issue in more detail (at least 10 characters)"
        )
    try:
        return pipeline.query_grievance(issue)
    except Exception as e:
        logger.error(f"Grievance error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process grievance")


def handle_scheme_match(pipeline: RAGPipeline, profile: dict) -> dict:
    try:
        schemes = pipeline.query_scheme_match(profile)
        return {"schemes": schemes}
    except Exception as e:
        logger.error(f"Scheme match error: {e}")
        raise HTTPException(status_code=500, detail="Failed to match schemes")
