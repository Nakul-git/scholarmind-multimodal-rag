import os

from langchain_core.documents import Document

from ingestion.fetch_arxiv import fetch_arxiv_papers
from ingestion.parse_pdf import parse_pdf
from ingestion.chunking import chunk_documents
from ingestion.embed_store import create_vector_db, load_vector_db
from ingestion.deduplication import (
    remove_duplicate_images,
    remove_exact_duplicates,
    remove_near_duplicates,
)
from pipeline.rag_pipeline import ResearchRAGPipeline


def ingest_new_papers():
    topic = input("\nEnter arXiv search topic: ").strip()
    max_results = int(input("How many papers to download? ").strip())

    papers = fetch_arxiv_papers(
        query=topic,
        max_results=max_results
    )

    all_docs = []

    for paper in papers:
        print("\n===================================")
        print(f"📄 Processing paper: {paper['title']}")
        print("===================================")

        parsed_items = parse_pdf(
            pdf_path=paper["pdf_path"],
            paper_metadata=paper
        )

        # ✅ Remove duplicate image_reasoning entries before chunking
        parsed_items = remove_duplicate_images(parsed_items)

        # ✅ Chunk text + LLaVA image summaries
        docs = chunk_documents(parsed_items)

        # ✅ Remove duplicate text chunks
        docs = remove_exact_duplicates(docs)

        # ✅ Remove near-duplicate chunks
        docs = remove_near_duplicates(docs, threshold=0.90)

        all_docs.extend(docs)

    # ✅ Global dedup across all papers
    print("\n🧹 Running global deduplication across all papers...")
    all_docs = remove_exact_duplicates(all_docs)
    all_docs = remove_near_duplicates(all_docs, threshold=0.90)

    print(f"\n✅ Final chunks to embed: {len(all_docs)}")

    print("\n🧠 Creating vector database...")
    db = create_vector_db(all_docs)

    return db, all_docs


def load_existing_docs_from_chroma(db):
    """
    Loads documents from Chroma for BM25.
    BM25 needs raw documents, not only vector search.
    """

    raw = db.get(include=["documents", "metadatas"])

    docs = []

    for text, metadata in zip(raw["documents"], raw["metadatas"]):
        docs.append(
            Document(
                page_content=text,
                metadata=metadata
            )
        )

    return docs


def chat_loop(db, all_docs):
    rag = ResearchRAGPipeline(
        db=db,
        all_docs=all_docs
    )

    print("\n🤖 Research Paper RAG Ready!")
    print("Ask questions about the papers.")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Bye!")
            break

        answer = rag.ask(question)

        print(answer)


def main():
    print("""
========================================
🧠 arXiv Research Paper RAG
Text + Images + LLaVA + Hybrid Search
Deduplication Enabled
========================================

1. Ingest new arXiv papers
2. Use existing vector database
""")

    choice = input("Choose option 1 or 2: ").strip()

    if choice == "1":
        db, all_docs = ingest_new_papers()

    elif choice == "2":
        if not os.path.exists("data/embeddings"):
            print("❌ No existing vector database found.")
            return

        db = load_vector_db()
        all_docs = load_existing_docs_from_chroma(db)

    else:
        print("❌ Invalid choice.")
        return

    chat_loop(db, all_docs)


if __name__ == "__main__":
    main()