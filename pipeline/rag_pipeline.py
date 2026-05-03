import os

from core.config import SETTINGS
from core.logging_utils import append_log_line, write_json
from core.monitoring import PipelineMonitor
from core.security import check_pii, check_prompt_injection, validate_query
from llm.generator import generate_answer
from llm.prompt import build_final_prompt
from retrieval.hybrid_search import hybrid_search, reciprocal_rank_fusion
from retrieval.multi_query import generate_multi_queries
from retrieval.query_understanding import apply_metadata_filter, build_metadata_filter, classify_query
from retrieval.reranker import MiniLMReranker


class ResearchRAGPipeline:
    def __init__(self, db, all_docs):
        self.db = db
        self.all_docs = all_docs
        self.reranker = MiniLMReranker()
        self.logs_dir = SETTINGS.logs_dir
        os.makedirs(self.logs_dir, exist_ok=True)

    def format_sources(self, docs):
        sources = []
        for i, doc in enumerate(docs, start=1):
            meta = doc.metadata
            source_text = (
                f"[Chunk {i}]\n"
                f"Source: {meta.get('title', 'Unknown paper')}\n"
                f"Page: {meta.get('page', 'Unknown page')}\n"
                f"Chunk type: {meta.get('type', 'unknown')}\n"
                f"PDF: {meta.get('source', 'Unknown source')}"
            )
            if meta.get("image_path"):
                source_text += f"\nImage path: {meta.get('image_path')}"
            sources.append(source_text)
        return "\n\n".join(sources)

    def _context_validation(self, docs):
        docs = [d for d in docs if d.page_content and len(d.page_content.strip()) > 30]
        return docs[: SETTINGS.final_top_k]

    def ask(self, question: str):
        mon = PipelineMonitor()
        append_log_line(os.path.join(self.logs_dir, "pipeline_steps.log"), f"Start query: {question}")

        with mon.step("query_validation"):
            ok, msg = validate_query(question)
            if not ok:
                return f"Query rejected: {msg}"
            ok, msg = check_prompt_injection(question)
            if not ok:
                return f"Query rejected: {msg}"

        with mon.step("query_understanding"):
            query_class = classify_query(question)
            metadata_filter = build_metadata_filter(query_class, question)

        with mon.step("multi_query"):
            queries = generate_multi_queries(question)
            write_json(os.path.join(self.logs_dir, "multi_queries.json"), {"question": question, "queries": queries})

        with mon.step("retrieval"):
            all_result_lists = []
            retrieved_snapshot = []
            for query in queries:
                docs = hybrid_search(
                    db=self.db,
                    query=query,
                    all_docs=self.all_docs,
                    top_k=SETTINGS.retriever_top_k,
                    metadata_filter=metadata_filter,
                )
                docs = apply_metadata_filter(docs, metadata_filter)
                all_result_lists.append(docs)
                retrieved_snapshot.append(
                    {
                        "query": query,
                        "results": [
                            {"content": d.page_content[:300], "metadata": d.metadata} for d in docs
                        ],
                    }
                )
            write_json(os.path.join(self.logs_dir, "retrieved_chunks.json"), retrieved_snapshot)

        with mon.step("rrf"):
            fused_docs = reciprocal_rank_fusion(all_result_lists)
            if not fused_docs:
                mon.counters["retrieval_failures"] += 1

        with mon.step("rerank"):
            top_docs = self.reranker.rerank(query=question, docs=fused_docs, top_k=SETTINGS.final_top_k)
            write_json(
                os.path.join(self.logs_dir, "reranked_chunks.json"),
                [{"content": d.page_content[:500], "metadata": d.metadata} for d in top_docs],
            )

        with mon.step("context_validation"):
            top_docs = self._context_validation(top_docs)

        with mon.step("prompt_building"):
            prompt = build_final_prompt(question, top_docs)
            with open(os.path.join(self.logs_dir, "final_prompt.txt"), "w", encoding="utf-8") as f:
                f.write(prompt)

        with mon.step("generation"):
            answer, model_used = generate_answer(prompt)
            if not answer.strip():
                mon.counters["empty_responses"] += 1

        with mon.step("output_processing"):
            if SETTINGS.enable_pii_check:
                pii_ok, _ = check_pii(answer)
                if not pii_ok:
                    answer = "Answer blocked due to potential sensitive content."

            sources = self.format_sources(top_docs)
            final_answer = (
                "\n================ ANSWER ================\n\n"
                f"{answer}\n\n"
                "================ SOURCES ================\n\n"
                f"{sources}\n"
            )

            with open(os.path.join(self.logs_dir, "final_answer.txt"), "w", encoding="utf-8") as f:
                f.write(final_answer)
            write_json(os.path.join(self.logs_dir, "model_used.json"), {"model": model_used})

        mon.save(self.logs_dir)
        append_log_line(os.path.join(self.logs_dir, "pipeline_steps.log"), "Query completed")

        return final_answer
