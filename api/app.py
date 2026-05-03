import os
from datetime import datetime

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from ingestion.embed_store import load_vector_db
from main import load_existing_docs_from_chroma
from pipeline.rag_pipeline import ResearchRAGPipeline


app = FastAPI(title="arXiv Production Multimodal RAG")


class QueryRequest(BaseModel):
    question: str
    user_id: str = "anonymous"
    tenant_id: str | None = None
    role: str = "user"


class QueryResponse(BaseModel):
    answer: str


class FeedbackRequest(BaseModel):
    user_id: str
    tenant_id: str = "public"
    rating: str
    question: str = ""
    answer: str = ""
    correction: str = ""


def require_api_key(x_api_key: str = Header(default="")):
    expected = os.getenv("RAG_API_KEY", "")
    if expected and x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid API key")


db = load_vector_db()
all_docs = load_existing_docs_from_chroma(db)
pipeline = ResearchRAGPipeline(db=db, all_docs=all_docs)


@app.get("/")
def home():
    return {
        "name": "ScholarMind API",
        "status": "ok",
        "endpoints": ["/health", "/query", "/feedback", "/docs"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse, dependencies=[Depends(require_api_key)])
def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Empty question")
    answer = pipeline.ask(req.question)
    return QueryResponse(answer=answer)


@app.post("/feedback", dependencies=[Depends(require_api_key)])
def feedback(req: FeedbackRequest):
    os.makedirs("logs/feedback", exist_ok=True)
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": req.user_id,
        "tenant_id": req.tenant_id,
        "rating": req.rating,
        "question": req.question,
        "answer": req.answer,
        "correction": req.correction,
    }
    with open("logs/feedback/feedback.jsonl", "a", encoding="utf-8") as f:
        import json

        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    return {"status": "saved"}
