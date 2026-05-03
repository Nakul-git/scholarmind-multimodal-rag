# 🧠 ScholarMind – arXiv Full Code Teaching Plan (No Skips)

A **deep-dive, engineering-grade learning and analysis framework** designed to fully understand and master the internal architecture of the **ScholarMind Multimodal RAG system**.

This plan ensures **zero black-box understanding** — every file, every function, and every data flow is explained with production-level clarity.

---

## 📌 Overview

This teaching plan walks through the entire repository in a **strict, structured sequence**, focusing on:

- 🔍 Understanding *what each file does*
- 🧠 Knowing *why it exists*
- 🔄 Tracing *data flow across modules*
- 🔗 Learning *how components are connected*

The goal is to transform this project from **"something you built" → "something you fully understand like an engineer."**

---

## 🎯 Teaching Methodology

| Aspect | Approach |
|------|--------|
| 🔍 Depth | Line-by-line code explanation |
| 📂 Pacing | Folder-by-folder sessions |
| 🚀 Start Order | `main.py → pipeline/ → api/` |

Each session is designed to be:
- Incremental  
- Practical  
- Debug-focused  
- Interview-ready  

---

## 🧩 What You Will Learn Per File

For every Python file, the breakdown includes:

- 📦 **Imports & Dependencies**  
  Why each library/module is used  

- ⚙️ **Global Configurations**  
  Environment variables, constants, settings  

- 🧠 **Function & Class Logic**  
  Line-by-line explanation of behavior  

- 🔄 **Inputs & Outputs**  
  What goes in, what comes out  

- 💥 **Side Effects**  
  File writes, DB operations, API/model calls  

- ⚠️ **Failure Modes**  
  Edge cases, common bugs, failure points  

- 🔗 **System Integration**  
  How the file connects to the runtime flow  

---

## 🏗️ Full Walkthrough Plan

### 🚀 1. Runtime Spine (Core Execution Flow)

This is the **heart of the system** — how everything runs.

- main.py
- pipeline/rag_pipeline.py
- api/app.py
- streamlit_app.py

---

### 📥 2. Ingestion Layer (Data Processing Pipeline)

Handles **data collection, parsing, and embedding**

**ingestion**

- fetch_arxiv.py
─ parse_pdf.py
─ image_reasoning.py
─ chunking.py
─ deduplication.py
─ embed_store.py
─ parser.py
─ metadata.py
─ trust_scoring.py
─ index_management.py

🔍 Key Concepts:
- PDF parsing (text + images)
- OCR + image reasoning (LLaVA)
- Chunking strategies
- Embedding pipelines (ChromaDB)
- Data validation & trust scoring

---

### 🔍 3. Retrieval Layer (Search & Ranking)

Responsible for **finding the best context**

**retrieval**

─ multi_query.py
─ hybrid_search.py
─ reranker.py
─ query_understanding.py
─ query_classifier.py
─ filters.py
─ context_validator.py
─ context_optimizer.py

🔍 Key Concepts:
- Multi-query expansion
- Hybrid search (Vector + BM25)
- Reranking (MiniLM / CrossEncoder)
- Query classification
- Context filtering & optimization

---

### 🤖 4. LLM Layer (Reasoning Engine)

Handles **prompting and final answer generation**

**llm**

─ prompt.py
─ prompt_builder.py
─ prompt_versions/*
─ generator.py
─ model_router.py
─ guardrails.py
─ output_validator.py


🔍 Key Concepts:
- Prompt engineering
- Model routing (Ollama/OpenAI)
- Output validation
- Guardrails & hallucination control

---

### 🛡️ 5. System Layers (Production Readiness)

- security
- safety
- reliability
- cache
- observability
- core
- config/settings.py

🔍 Covers:
- Security & access control
- Safety filters
- Caching strategies
- Monitoring & logging
- Core configurations

---

### 📊 6. Evaluation & Experimentation

governance/*
feedback/*
evaluation/*
experiments/*
scripts/*
tests/*
