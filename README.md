# 🧠 ScholarMind – arXiv Research Paper RAG system + LLMOps

> **A deep-dive, engineering-grade learning and analysis framework** for fully understanding and mastering the internal architecture of the ScholarMind Multimodal RAG system.

This plan ensures **zero black-box understanding** — every file, every function, and every data flow is explained with production-level clarity.

---

## 📌 Overview

This teaching plan walks through the entire repository in a **strict, structured sequence**, focusing on:

- 🔍 Understanding *what each file does*
- 🧠 Knowing *why it exists*
- 🔄 Tracing *data flow across modules*
- 🔗 Learning *how components are connected*

The goal is to transform this project from **"something you built"** → **"something you fully understand like an engineer."**

---

## 🎯 Teaching Methodology

| Aspect | Approach |
|--------|----------|
| 🔍 Depth | Line-by-line code explanation |
| 📂 Pacing | Folder-by-folder sessions |
| 🚀 Start Order | `main.py → pipeline/ → api/` |

Each session is designed to be **incremental**, **practical**, **debug-focused**, and **interview-ready**.

---

## 🧩 What You Will Learn Per File

For every Python file, the breakdown includes:

| Category | Description |
|----------|-------------|
| 📦 **Imports & Dependencies** | Why each library/module is used |
| ⚙️ **Global Configurations** | Environment variables, constants, settings |
| 🧠 **Function & Class Logic** | Line-by-line explanation of behavior |
| 🔄 **Inputs & Outputs** | What goes in, what comes out |
| 💥 **Side Effects** | File writes, DB operations, API/model calls |
| ⚠️ **Failure Modes** | Edge cases, common bugs, failure points |
| 🔗 **System Integration** | How the file connects to the runtime flow |

---

## 🏗️ Full Walkthrough Plan

### 🚀 1. Runtime Spine — Core Execution Flow

> The **heart of the system** — how everything runs.

```
main.py
pipeline/rag_pipeline.py
api/app.py
streamlit_app.py
```

---

### 📥 2. Ingestion Layer — Data Processing Pipeline

> Handles **data collection, parsing, and embedding**.

```
ingestion/
├── fetch_arxiv.py
├── parse_pdf.py
├── image_reasoning.py
├── chunking.py
├── deduplication.py
├── embed_store.py
├── parser.py
├── metadata.py
├── trust_scoring.py
├── index_management.py
└── loaders/*
```

**Key Concepts:**
- PDF parsing (text + images)
- OCR + image reasoning (LLaVA)
- Chunking strategies
- Embedding pipelines (ChromaDB)
- Data validation & trust scoring

---

### 🔍 3. Retrieval Layer — Search & Ranking

> Responsible for **finding the best context**.

```
retrieval/
├── multi_query.py
├── hybrid_search.py
├── reranker.py
├── query_understanding.py
├── query_classifier.py
├── filters.py
├── context_validator.py
└── context_optimizer.py
```

**Key Concepts:**
- Multi-query expansion
- Hybrid search (Vector + BM25)
- Reranking (MiniLM / CrossEncoder)
- Query classification
- Context filtering & optimization

---

### 🤖 4. LLM Layer — Reasoning Engine

> Handles **prompting and final answer generation**.

```
llm/
├── prompt.py
├── prompt_builder.py
├── prompt_versions/*
├── generator.py
├── model_router.py
├── guardrails.py
└── output_validator.py
```

**Key Concepts:**
- Prompt engineering
- Model routing (Ollama / OpenAI)
- Output validation
- Guardrails & hallucination control

---

### 🛡️ 5. System Layers — Production Readiness

```
security/*
safety/*
reliability/*
cache/*
observability/*
core/*
config/settings.py
```

**Covers:**
- Security & access control
- Safety filters
- Caching strategies
- Monitoring & logging
- Core configurations

---

### 📊 6. Evaluation & Experimentation

```
governance/*
feedback/*
evaluation/*
experiments/*
scripts/*
tests/*
```

**Covers:**
- Model evaluation pipelines
- Feedback loops
- Experiment tracking
- Testing strategies

---

### 🗂️ 7. Data & Logs Understanding

```
data/*
logs/*
```

**Covers:**
- Data storage formats
- Embeddings structure
- Log generation & debugging

---

## 📚 Per-Session Structure

Each learning session follows this format:

### 🔄 Execution Flow
```
Entry → Function Calls → Processing → Output
```

### 📂 File Breakdown
- Line-by-line explanation
- Purpose of each component

### 💾 State Changes
- Memory updates
- File system changes
- DB writes
- Logs generated

### ❓ Understanding Check
- Questions to validate learning

### 🔁 Recap
- Key takeaways
- What's next

---

## ✅ Learning Outcomes

By the end of this plan, you will be able to:

**🔎 Trace a query end-to-end**
```
UI/API → Retrieval → LLM → Final Answer
```

**📥 Understand the full ingestion flow**
```
Raw PDF → Parsing → Chunking → Embedding → Vector DB
```

**🧩 Explain system architecture clearly**

**🛠️ Modify system behavior:**
- Prompts
- Retrieval logic
- Safety rules
- Caching
- Logging

**🐛 Debug efficiently:**
- Identify failure points
- Use logs correctly
- Fix issues systematically

---

## ⚙️ Assumptions

- **Focus is on:** `.py` files and core project files (`README.md`, `.env`, `requirements.txt`)
- **"No skips" means:** Every meaningful line is explained — no abstraction without clarity
- **Priority:** ✅ Real working implementation — ❌ Not just theoretical design

---

## 🚀 End Goal

This is not just a walkthrough.

By completing this plan, you will:

- Think like a **RAG System Engineer**
- Build **production-ready AI systems**
- Master **Multimodal Retrieval (Text + Image + LLM)**

---

> 🔥 **ScholarMind is not just a project — it's a system you can fully own, explain, and extend.**
