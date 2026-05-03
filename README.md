# 🧠 ScholarMind — Multimodal Research Intelligence System

> An **engineering-grade, production-ready RAG system** that fetches, parses, understands, and reasons over arXiv research papers — combining text, images, and LLMs into a unified multimodal intelligence pipeline.

---

## 📌 What is ScholarMind?

ScholarMind is a **Multimodal Retrieval-Augmented Generation (RAG) system** built for deep research intelligence over scientific papers. It ingests arXiv PDFs, extracts both text and visual content, stores rich embeddings, and generates grounded answers using a full LLMOps-grade backend.

This is not a wrapper around a search API — it is a **complete AI system** with ingestion, retrieval, reasoning, safety, caching, observability, and evaluation layers built from the ground up.

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
│   Retrieval Layer   │  query expansion → hybrid search → rerank → filter
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│     LLM Layer       │  prompt building → model routing → guardrails → output
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│   API / UI Layer    │  FastAPI (REST) + Streamlit (UI)
└─────────────────────┘
```

---

## 🏗️ Repository Structure

### 🚀 Runtime Spine — Core Execution

```
main.py                    # Application entry point
pipeline/rag_pipeline.py   # End-to-end RAG orchestration
api/app.py                 # FastAPI REST interface
streamlit_app.py           # Streamlit web UI
```

---

### 📥 Ingestion Layer — Data Processing Pipeline

Handles the full journey from raw PDF to searchable embeddings.

```
ingestion/
├── fetch_arxiv.py         # Fetches papers from the arXiv API
├── parse_pdf.py           # Extracts text and structure from PDFs
├── image_reasoning.py     # OCR + visual understanding via LLaVA
├── chunking.py            # Splits content into retrieval-ready chunks
├── deduplication.py       # Removes duplicate content before indexing
├── embed_store.py         # Generates embeddings and stores in ChromaDB
├── parser.py              # Low-level document parsing utilities
├── metadata.py            # Extracts and structures paper metadata
├── trust_scoring.py       # Scores source reliability
├── index_management.py    # Manages ChromaDB index lifecycle
└── loaders/               # Format-specific document loaders
```

**Pipeline:**
```
Raw PDF → parse_pdf → image_reasoning → chunking → deduplication → embed_store → ChromaDB
```

---

### 🔍 Retrieval Layer — Search & Ranking

Finds the most relevant context for any query using hybrid, multi-stage retrieval.

```
retrieval/
├── multi_query.py         # Expands a single query into multiple search angles
├── hybrid_search.py       # Combines dense (vector) + sparse (BM25) search
├── reranker.py            # Cross-encoder reranking (MiniLM / CrossEncoder)
├── query_understanding.py # Parses and enriches query intent
├── query_classifier.py    # Routes query to the appropriate retrieval strategy
├── filters.py             # Metadata-based pre/post filtering
├── context_validator.py   # Validates retrieved chunks for relevance
└── context_optimizer.py   # Trims and optimizes context for the LLM window
```

**Pipeline:**
```
User Query → query_classifier → multi_query → hybrid_search → reranker → context_optimizer → LLM
```

---

### 🤖 LLM Layer — Reasoning Engine

Handles prompt construction, model selection, and safe output generation.

```
llm/
├── prompt.py              # Core prompt templates
├── prompt_builder.py      # Dynamically assembles prompts from context + query
├── prompt_versions/       # Versioned prompt history for A/B testing
├── generator.py           # Calls the LLM and streams the response
├── model_router.py        # Routes requests between Ollama / OpenAI backends
├── guardrails.py          # Input/output safety enforcement
└── output_validator.py    # Validates final answers for quality and grounding
```

**Pipeline:**
```
Context + Query → prompt_builder → model_router → generator → output_validator → Response
```

---

### 🛡️ System Layers — Production Readiness

```
security/        # Authentication, authorization, rate limiting
safety/          # Content moderation and unsafe query handling
reliability/     # Retry logic, circuit breakers, fallback handling
cache/           # Query-level and embedding-level caching
observability/   # Logging, tracing, metrics collection
core/            # Shared utilities, base classes, interfaces
config/
└── settings.py  # Centralized configuration and environment management
```

---

### 📊 Evaluation & Experimentation

```
governance/      # Policy enforcement and compliance rules
feedback/        # User feedback collection and signal processing
evaluation/      # RAG evaluation metrics (faithfulness, relevance, recall)
experiments/     # Experiment tracking and comparison
scripts/         # Utility and automation scripts
tests/           # Unit, integration, and end-to-end test suites
```

---

### 🗂️ Data & Logs

```
data/            # Stored embeddings, paper metadata, processed chunks
logs/            # Runtime logs for debugging and audit trails
```

---

## 🔎 End-to-End Query Flow

```
1. User submits a research question via UI or API
        │
2. query_classifier identifies intent and scope
        │
3. multi_query expands it into parallel search queries
        │
4. hybrid_search runs dense + sparse retrieval over ChromaDB
        │
5. reranker scores and selects the top-k chunks
        │
6. context_optimizer trims context to fit the LLM window
        │
7. prompt_builder assembles the final prompt
        │
8. model_router sends it to Ollama (local) or OpenAI (cloud)
        │
9. guardrails + output_validator ensure safe, grounded output
        │
10. Response streamed back to user
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
| API | FastAPI |
| UI | Streamlit |
| Observability | Custom logging + metrics |

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
# Edit .env with your API keys and settings

# Run ingestion
python main.py --ingest

# Start the API
uvicorn api.app:app --reload

# Launch the UI
streamlit run streamlit_app.py
```

---

## ⚙️ Configuration

All system behaviour is controlled via `config/settings.py` and the `.env` file:

```env
ARXIV_QUERY=...          # Default arXiv search query
CHROMA_DB_PATH=...       # Path to ChromaDB storage
OLLAMA_BASE_URL=...      # Local Ollama endpoint
OPENAI_API_KEY=...       # Optional: OpenAI fallback
LOG_LEVEL=...            # Logging verbosity
```

---

> 🔥 **ScholarMind is a fully owned, fully understood, production-grade AI system — not just a project.**
