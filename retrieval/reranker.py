from sentence_transformers import CrossEncoder


class MiniLMReranker:
    def __init__(self):
        print("🎯 Loading MiniLM reranker...")
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query: str, docs, top_k: int = 5):
        """
        Rerank retrieved chunks using cross-encoder.
        """

        if not docs:
            return []

        pairs = [
            [query, doc.page_content]
            for doc in docs
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, score in ranked[:top_k]]