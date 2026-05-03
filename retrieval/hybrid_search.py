from rank_bm25 import BM25Okapi


def reciprocal_rank_fusion(result_lists, k=60):
    scores = {}
    for result_list in result_lists:
        for rank, doc in enumerate(result_list):
            key = (doc.page_content, str(doc.metadata))
            if key not in scores:
                scores[key] = {"doc": doc, "score": 0}
            scores[key]["score"] += 1 / (k + rank + 1)
    ranked = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    return [item["doc"] for item in ranked]


def bm25_search(query: str, docs, top_k: int = 8):
    if not docs:
        return []
    tokenized_docs = [doc.page_content.lower().split() for doc in docs]
    bm25 = BM25Okapi(tokenized_docs)
    scores = bm25.get_scores(query.lower().split())
    ranked_indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return [docs[i] for i in ranked_indexes[:top_k]]


def hybrid_search(db, query: str, all_docs, top_k: int = 8, metadata_filter=None):
    vector_docs = db.max_marginal_relevance_search(query=query, k=top_k, fetch_k=25)
    keyword_docs = bm25_search(query=query, docs=all_docs, top_k=top_k)

    if metadata_filter:
        vector_docs = [d for d in vector_docs if all(d.metadata.get(k) == v for k, v in metadata_filter.items())]
        keyword_docs = [d for d in keyword_docs if all(d.metadata.get(k) == v for k, v in metadata_filter.items())]

    fused_docs = reciprocal_rank_fusion([vector_docs, keyword_docs])
    return fused_docs[:top_k]
