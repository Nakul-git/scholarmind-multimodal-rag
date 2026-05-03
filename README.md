# 🧠 ScholarMind — Multimodal Research Intelligence System

> An **engineering-grade, production-ready RAG system** that fetches, parses, understands, and reasons over arXiv research papers — combining text, images, and LLMs into a unified multimodal intelligence pipeline with a **full LLMOps backend**.

---

## 📌 What is ScholarMind?

ScholarMind is a **Multimodal Retrieval-Augmented Generation (RAG) system** built for deep research intelligence over scientific papers. It ingests arXiv PDFs, extracts both text and visual content, stores rich embeddings, and generates grounded answers through a **production-grade LLMOps pipeline**.

This is not a wrapper around a search API — it is a **complete AI system** with ingestion, retrieval, reasoning, evaluation, and observability layers built from the ground up.

---

## ⚡ System Architecture — Full Flow

```
arXiv Papers (PDF)
       │
       ▼
┌─────────────────────┐
│   Ingestion Layer   │  fetch → parse → chunk → embed → store
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│   Vector Store      │  ChromaDB (dense) + BM25 (sparse)
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│   Retrieval Layer   │  query expansion → hybrid search → rerank
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│   LLMOps Layer      │  prompt versioning → model routing → guardrails → evaluation
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│     LLM Layer       │  prompt building → generation → response
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│     UI Layer        │  Streamlit (UI) + FastAPI (REST)
└─────────────────────┘
```

---

## 🏗️ Repository Structure

```
arXiv/
├── api/
│   └── app.py                    # FastAPI REST interface
│
├── core/
│   ├── cache.py                  # Query-level and embedding-level caching
│   ├── config.py                 # Centralized configuration management
│   ├── logging_utils.py          # Structured logging across all pipeline stages
│   ├── model_registry.py         # LLM model registration and management
│   ├── monitoring.py             # Runtime metrics and performance tracking
│   └── security.py               # Authentication, authorization, rate limiting
│
├── data/
│   ├── embeddings/               # Stored vector embeddings
│   ├── images/                   # Extracted paper images and figures
│   ├── parsed/                   # Processed and structured paper content
│   └── raw_papers/               # Original downloaded arXiv PDFs
│
├── evaluation/
│   ├── eval_questions.json       # Evaluation question bank
│   ├── evaluate_rag.py           # RAG evaluation — faithfulness, relevance, recall
│   └── experiment_tracking.py    # Experiment logging and comparison
│
├── ingestion/
│   ├── chunking.py               # Splits content into retrieval-ready chunks
│   ├── deduplication.py          # Removes duplicate content before indexing
│   ├── embed_store.py            # Generates embeddings and stores in ChromaDB
│   ├── fetch_arxiv.py            # Fetches papers from the arXiv API
│   ├── image_reasoning.py        # OCR + visual understanding via LLaVA
│   ├── index_management.py       # Manages ChromaDB index lifecycle
│   └── parse_pdf.py              # Extracts text and structure from PDFs
│
├── llm/
│   ├── generator.py              # Calls the LLM and streams the response
│   ├── prompt.py                 # Core prompt templates
│   └── prompt_versions.py        # Versioned prompt history for A/B testing
│
├── pipeline/
│   └── rag_pipeline.py           # End-to-end RAG orchestration
│
├── retrieval/
│   ├── hybrid_search.py          # Dense (vector) + sparse (BM25) search
│   ├── multi_query.py            # Expands a single query into multiple angles
│   ├── query_understanding.py    # Parses and enriches query intent
│   └── reranker.py               # Cross-encoder reranking (MiniLM / CrossEncoder)
│
├── logs/                         # Runtime logs for debugging and audit trails
├── main.py                       # Application entry point
├── streamlit_app.py              # Streamlit web UI
├── requirements.txt              # Python dependencies
└── .env.example                  # Environment variable template
```

---

## 🔍 Layer Breakdown

### 🚀 Runtime Spine — Core Execution

```
main.py                        # Entry point — boots the full system
pipeline/rag_pipeline.py       # Orchestrates the end-to-end RAG flow
api/app.py                     # FastAPI REST interface
streamlit_app.py               # Streamlit web UI
```

---

### 📥 Ingestion Layer

Handles the full journey from raw arXiv PDF to searchable embeddings.

```
ingestion/
├── fetch_arxiv.py             # Fetches papers from the arXiv API
├── parse_pdf.py               # Extracts text and structure from PDFs
├── image_reasoning.py         # OCR + visual understanding via LLaVA
├── chunking.py                # Splits content into retrieval-ready chunks
├── deduplication.py           # Removes duplicate content before indexing
├── embed_store.py             # Generates embeddings and stores in ChromaDB
└── index_management.py        # Manages ChromaDB index lifecycle
```

**Pipeline:**
```
Raw PDF → parse_pdf → image_reasoning → chunking → deduplication → embed_store → ChromaDB
```

---

### 🔍 Retrieval Layer

Finds the most relevant context using hybrid, multi-stage retrieval.

```
retrieval/
├── multi_query.py             # Expands a single query into multiple search angles
├── hybrid_search.py           # Dense (ChromaDB) + sparse (BM25) search
├── reranker.py                # Cross-encoder reranking (MiniLM / CrossEncoder)
└── query_understanding.py     # Parses and enriches query intent
```

**Pipeline:**
```
User Query → query_understanding → multi_query → hybrid_search → reranker → LLM
```

---

### 🤖 LLM Layer

Handles prompt construction and grounded answer generation.

```
llm/
├── prompt.py                  # Core prompt templates
├── prompt_versions.py         # Versioned prompt history for A/B testing
└── generator.py               # Calls the LLM and streams the response
```

**Pipeline:**
```
Context + Query → prompt (versioned) → generator → Response
```

---

### ⚙️ LLMOps Layer — Production AI Operations

> The operational backbone that makes ScholarMind **production-ready** — not just a demo.

```
core/
├── cache.py                   # Query-level and embedding-level caching
├── config.py                  # Centralized environment and settings management
├── logging_utils.py           # Structured logging across every pipeline stage
├── model_registry.py          # LLM model registration, versioning, and routing
├── monitoring.py              # Latency, retrieval quality, and model performance
└── security.py                # Auth, authorization, and rate limiting

llm/
└── prompt_versions.py         # Full prompt history — rollback and A/B comparison

evaluation/
├── evaluate_rag.py            # Faithfulness, relevance, and recall scoring
├── experiment_tracking.py     # Tracks and compares experiments over time
└── eval_questions.json        # Curated evaluation question bank

logs/                          # Audit trail and runtime logs
```

**LLMOps Flow:**
```
Query In
   │
   ├── cache.py        → cache hit? return instantly
   │
   ├── prompt.py       → versioned prompt assembly
   │
   ├── model_registry  → route to correct model
   │
   ├── generator.py    → streamed LLM response
   │
   ├── monitoring.py   → log latency + metrics
   │
   ├── logging_utils   → structured audit log
   │
   └── evaluate_rag    → faithfulness · relevance · recall
```

**Key LLMOps Capabilities:**

| Capability | File |
|------------|------|
| 🔀 Model Routing & Registry | `core/model_registry.py` |
| 📝 Prompt Versioning | `llm/prompt_versions.py` |
| ⚡ Caching | `core/cache.py` |
| 🔭 Observability & Logging | `core/logging_utils.py` + `logs/` |
| 📊 Performance Monitoring | `core/monitoring.py` |
| 🛡️ Security & Auth | `core/security.py` |
| ✅ RAG Evaluation | `evaluation/evaluate_rag.py` |
| 🧪 Experiment Tracking | `evaluation/experiment_tracking.py` |
| ⚙️ Config Management | `core/config.py` |

---

### 🗂️ Data Store

```
data/
├── embeddings/                # Stored vector embeddings (ChromaDB)
├── images/                    # Extracted paper figures and diagrams
├── parsed/                    # Processed and structured paper content
└── raw_papers/                # Original downloaded arXiv PDFs
```

---

## 🔎 End-to-End Query Flow

```
1.  User submits a research question via Streamlit UI or API
         │
2.  security.py validates the request
         │
3.  cache.py checks for a cached response → returns instantly on hit
         │
4.  query_understanding.py parses and enriches query intent
         │
5.  multi_query.py expands it into parallel search queries
         │
6.  hybrid_search.py runs dense + sparse retrieval over ChromaDB
         │
7.  reranker.py scores and selects the top-k chunks
         │
8.  prompt.py assembles prompt from versioned template
         │
9.  model_registry.py routes to the correct LLM backend
         │
10. generator.py streams the response
         │
11. monitoring.py logs latency and performance metrics
         │
12. logging_utils.py writes structured audit log
         │
13. evaluate_rag.py scores faithfulness, relevance, recall
         │
14. Response streamed back to user
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| PDF Parsing | PyMuPDF, pdfplumber |
| Image Reasoning | LLaVA (multimodal LLM) |
| Embeddings | Sentence Transformers |
| Vector Store | ChromaDB |
| Sparse Search | BM25 |
| Reranking | MiniLM / CrossEncoder |
| LLM Backend | Ollama (local) / OpenAI |
| Prompt Versioning | `llm/prompt_versions.py` |
| Model Registry | `core/model_registry.py` |
| Caching | `core/cache.py` |
| Monitoring | `core/monitoring.py` |
| Observability | `core/logging_utils.py` + `logs/` |
| Security | `core/security.py` |
| Evaluation | `evaluation/evaluate_rag.py` |
| Experiment Tracking | `evaluation/experiment_tracking.py` |
| API | FastAPI |
| UI | Streamlit |

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/your-username/scholarmind.git
cd scholarmind

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run ingestion
python main.py --ingest

# Start the API
uvicorn api.app:app --reload

# Launch the UI
streamlit run streamlit_app.py
```

---

## ⚙️ Configuration

All system behaviour is controlled via `core/config.py` and the `.env` file:

```env
ARXIV_QUERY=...          # Default arXiv search query
CHROMA_DB_PATH=...       # Path to ChromaDB storage
OLLAMA_BASE_URL=...      # Local Ollama endpoint
OPENAI_API_KEY=...       # Optional: OpenAI fallback
LOG_LEVEL=...            # Logging verbosity
```

---

> 🔥 **ScholarMind is not just a RAG project — it's a fully operational AI system with a complete LLMOps backbone, built to production standard from the ground up.**
