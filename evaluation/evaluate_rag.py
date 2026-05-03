import json
import os
import sys

# Allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingestion.embed_store import load_vector_db
from main import load_existing_docs_from_chroma
from pipeline.rag_pipeline import ResearchRAGPipeline


EVAL_FILE = "evaluation/eval_questions.json"


def load_eval_questions():
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def keyword_score(text, expected_keywords):
    """
    Simple keyword-based faithfulness / coverage score.
    """

    text_lower = text.lower()

    matched = []

    for keyword in expected_keywords:
        if keyword.lower() in text_lower:
            matched.append(keyword)

    score = len(matched) / len(expected_keywords) if expected_keywords else 0

    return score, matched


def source_correctness_score(answer):
    """
    Checks whether answer contains citations/sources.
    """

    has_chunk_citation = "[Chunk" in answer
    has_sources_section = "SOURCES" in answer
    has_page = "Page:" in answer or "Page " in answer

    score = sum([has_chunk_citation, has_sources_section, has_page]) / 3

    return score


def hallucination_risk_score(answer):
    """
    Simple heuristic:
    Lower risk if answer says context is insufficient when unsure,
    and uses citations.
    """

    answer_lower = answer.lower()

    risky_phrases = [
        "obviously",
        "clearly proves",
        "always",
        "never",
        "guarantees",
        "without any doubt"
    ]

    risk_hits = [p for p in risky_phrases if p in answer_lower]

    if "provided paper context does not contain enough information" in answer_lower:
        return 0.0, risk_hits

    citation_present = "[chunk" in answer_lower

    risk = len(risk_hits) * 0.2

    if not citation_present:
        risk += 0.5

    return min(risk, 1.0), risk_hits


def run_evaluation():
    print("\n🧪 Loading vector database...")
    db = load_vector_db()
    all_docs = load_existing_docs_from_chroma(db)

    rag = ResearchRAGPipeline(db=db, all_docs=all_docs)

    questions = load_eval_questions()

    results = []

    for idx, item in enumerate(questions, start=1):
        question = item["question"]
        expected_keywords = item["expected_keywords"]

        print("\n====================================")
        print(f"🧪 Eval Question {idx}")
        print(f"Q: {question}")
        print("====================================")

        answer = rag.ask(question)

        keyword_coverage, matched_keywords = keyword_score(
            answer,
            expected_keywords
        )

        source_score = source_correctness_score(answer)

        hallucination_risk, risky_phrases = hallucination_risk_score(answer)

        result = {
            "question": question,
            "expected_keywords": expected_keywords,
            "matched_keywords": matched_keywords,
            "keyword_coverage": round(keyword_coverage, 2),
            "source_correctness": round(source_score, 2),
            "hallucination_risk": round(hallucination_risk, 2),
            "risky_phrases": risky_phrases,
            "answer": answer
        }

        results.append(result)

        print("\n📊 Scores:")
        print(f"Keyword coverage: {keyword_coverage:.2f}")
        print(f"Source correctness: {source_score:.2f}")
        print(f"Hallucination risk: {hallucination_risk:.2f}")
        print(f"Matched keywords: {matched_keywords}")

    os.makedirs("logs", exist_ok=True)

    output_path = "logs/evaluation_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n✅ Evaluation complete!")
    print(f"📁 Results saved to: {output_path}")


if __name__ == "__main__":
    run_evaluation()