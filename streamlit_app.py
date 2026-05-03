import contextlib
import io
import json
import os
import re
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st

# Reduce startup noise from transformers advisory path warnings.
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")

from evaluation.evaluate_rag import run_evaluation
from ingestion.chunking import chunk_documents
from ingestion.deduplication import remove_exact_duplicates, remove_near_duplicates, remove_duplicate_images
from ingestion.embed_store import create_vector_db, load_vector_db
from ingestion.fetch_arxiv import fetch_arxiv_papers
from ingestion.parse_pdf import parse_pdf


st.set_page_config(
    page_title="ScholarMind - Multimodal Research Intelligence System",
    page_icon="SM",
    layout="wide",
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_qa" not in st.session_state:
    st.session_state.last_qa = {"question": "", "answer": ""}
if "ingestion_log" not in st.session_state:
    st.session_state.ingestion_log = ""
if "last_ingested_chunks" not in st.session_state:
    st.session_state.last_ingested_chunks = 0

st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(180deg, #f6f8fb 0%, #eef2f7 100%);
        }
        .hero {
            padding: 1rem 1.2rem;
            border-radius: 16px;
            background: linear-gradient(120deg, #0f172a 0%, #1f2937 55%, #334155 100%);
            color: #f8fafc;
            border: 1px solid #334155;
            margin-bottom: 1rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.1rem;
            line-height: 1.2;
            letter-spacing: 0.2px;
        }
        .hero p {
            margin: 0.55rem 0 0;
            color: #cbd5e1;
            font-size: 1.02rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def _headers(api_key: str):
    return {"x-api-key": api_key} if api_key else {}


def ping_health(base_url: str):
    try:
        r = requests.get(f"{base_url}/health", timeout=4)
        return r.status_code, r.text
    except Exception as exc:
        return None, str(exc)


def list_log_files():
    log_dir = Path("logs")
    if not log_dir.exists():
        return []
    return sorted([p for p in log_dir.iterdir() if p.is_file()], key=lambda x: x.name)


def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return "Unable to read file"


def parse_answer_sections(answer: str):
    parts = re.split(r"=+\s*SOURCES\s*=+", answer, flags=re.IGNORECASE)
    body = parts[0].strip()
    sources = parts[1].strip() if len(parts) > 1 else ""
    body = re.sub(r"^=+\s*ANSWER\s*=+", "", body, flags=re.IGNORECASE).strip()
    return body, sources


def run_arxiv_ingestion(topic: str, max_results: int):
    log_buffer = io.StringIO()
    with contextlib.redirect_stdout(log_buffer), contextlib.redirect_stderr(log_buffer):
        papers = fetch_arxiv_papers(topic, max_results)
        all_docs = []
        for paper in papers:
            parsed_items = parse_pdf(pdf_path=paper["pdf_path"], paper_metadata=paper)
            parsed_items = remove_duplicate_images(parsed_items)
            docs = chunk_documents(parsed_items)
            docs = remove_exact_duplicates(docs)
            docs = remove_near_duplicates(docs, threshold=0.90)
            all_docs.extend(docs)

        all_docs = remove_exact_duplicates(all_docs)
        all_docs = remove_near_duplicates(all_docs, threshold=0.90)

        if all_docs:
            # Rebuilds/updates persisted Chroma collection with new docs
            create_vector_db(all_docs)

    return len(all_docs), log_buffer.getvalue()


st.markdown(
    """
    <div class="hero">
        <h1>ScholarMind - Multimodal Research Intelligence System</h1>
        <p>Grounded retrieval, cited generation, ingestion operations, and LLMOps visibility.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("System Settings")
    api_base = st.text_input("FastAPI Base URL", value="http://127.0.0.1:8000")
    api_key = st.text_input("API Key (x-api-key)", value="", type="password")
    user_id = st.text_input("User ID", value="nakul")
    tenant_id = st.text_input("Tenant ID", value="public")
    role = st.selectbox("Role", ["user", "admin"], index=0)

    st.markdown("### Quick Links")
    st.markdown(f"- [API Home]({api_base}/)")
    st.markdown(f"- [Health]({api_base}/health)")
    st.markdown(f"- [Docs]({api_base}/docs)")

code, details = ping_health(api_base)
status_col1, status_col2, status_col3 = st.columns(3)
status_col1.metric("Backend", "Online" if code == 200 else "Offline")
status_col2.metric("HTTP", str(code) if code is not None else "N/A")
status_col3.metric("Timestamp", datetime.now().strftime("%H:%M:%S"))

with st.expander("Backend Details", expanded=False):
    st.code(details)

tab_query, tab_ingest, tab_eval, tab_ops = st.tabs(["Research QA", "Ingestion", "Evaluation", "Observability"])

with tab_query:
    st.subheader("Ask Grounded Research Questions")
    question = st.text_area("Question", height=120)
    send = st.button("Generate Answer", type="primary")

    if send and question.strip():
        payload = {"question": question, "user_id": user_id, "tenant_id": tenant_id, "role": role}
        try:
            r = requests.post(
                f"{api_base}/query",
                headers={"Content-Type": "application/json", **_headers(api_key)},
                data=json.dumps(payload),
                timeout=120,
            )
            if r.status_code == 200:
                answer = r.json().get("answer", "")
                body, sources = parse_answer_sections(answer)
                st.session_state.last_qa = {"question": question, "answer": answer}
                st.session_state.chat_history.append({"ts": datetime.now().isoformat(), "question": question, "answer": answer})

                st.markdown("### Answer")
                st.write(body)
                st.markdown("### Citations and Sources")
                st.code(sources if sources else "No structured sources section found.")
            else:
                st.error(f"Request failed ({r.status_code})")
                st.code(r.text)
        except Exception as exc:
            st.error(f"Failed to call backend: {exc}")

    st.markdown("### Session History")
    if not st.session_state.chat_history:
        st.info("No queries yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.chat_history[-10:]), start=1):
            with st.expander(f"{i}. {item['question'][:80]}"):
                st.caption(item["ts"])
                st.write(item["answer"])

    st.markdown("### Feedback")
    f1, f2 = st.columns(2)
    up = f1.button("Thumbs Up")
    down = f2.button("Thumbs Down")
    correction = st.text_area("Correction (optional)", height=80)
    submit_feedback = st.button("Submit Feedback")

    if up or down or submit_feedback:
        rating = "up" if up else "down"
        if submit_feedback and not rating:
            rating = "down" if correction.strip() else "up"
        if not st.session_state.last_qa["question"]:
            st.warning("Ask at least one question before sending feedback.")
        else:
            fb_payload = {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "rating": rating,
                "question": st.session_state.last_qa["question"],
                "answer": st.session_state.last_qa["answer"],
                "correction": correction,
            }
            try:
                fr = requests.post(
                    f"{api_base}/feedback",
                    headers={"Content-Type": "application/json", **_headers(api_key)},
                    data=json.dumps(fb_payload),
                    timeout=30,
                )
                if fr.status_code == 200:
                    st.success("Feedback saved")
                else:
                    st.error(f"Feedback failed ({fr.status_code})")
                    st.code(fr.text)
            except Exception as exc:
                st.error(f"Feedback error: {exc}")

with tab_ingest:
    st.subheader("Ingestion Workspace")
    query = st.text_input("arXiv Topic Query", value="transformer")
    max_results = st.slider("Max Papers", 1, 20, 3)
    if st.button("Run Ingestion", type="primary"):
        with st.spinner("Fetching, parsing, chunking, and indexing papers..."):
            try:
                count, run_log = run_arxiv_ingestion(query, max_results)
                st.session_state.last_ingested_chunks = count
                st.session_state.ingestion_log = run_log
                st.success(f"Ingestion complete. Indexed chunks: {count}")
            except Exception as exc:
                st.error(f"Ingestion failed: {exc}")

    if st.session_state.ingestion_log:
        st.markdown("### Ingestion Live Log")
        st.code(st.session_state.ingestion_log)
        st.caption(f"Latest indexed chunks: {st.session_state.last_ingested_chunks}")

with tab_eval:
    st.subheader("Evaluation Pipeline")
    if st.button("Run Evaluation", type="primary"):
        try:
            run_evaluation()
            st.success("Evaluation completed")
        except Exception as exc:
            st.error(f"Evaluation failed: {exc}")

    eval_path = Path("logs/evaluation_results.json")
    if eval_path.exists():
        try:
            st.json(json.loads(eval_path.read_text(encoding="utf-8")))
        except Exception:
            st.code(eval_path.read_text(encoding="utf-8"))

with tab_ops:
    st.subheader("Logs, Traces, and Runtime Artifacts")
    files = list_log_files()
    if not files:
        st.info("No log files found in `logs/` yet.")
    else:
        selected = st.selectbox("Select log file", files, format_func=lambda p: p.name)
        content = read_text(selected)
        if selected.suffix.lower() == ".json":
            try:
                st.json(json.loads(content))
            except Exception:
                st.code(content)
        else:
            st.code(content)
