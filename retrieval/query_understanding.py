from typing import Dict, List


def classify_query(query: str) -> str:
    q = query.lower()
    if any(x in q for x in ["figure", "image", "diagram", "table"]):
        return "figure"
    if any(x in q for x in ["method", "approach", "algorithm"]):
        return "method"
    if any(x in q for x in ["compare", "difference", "vs"]):
        return "comparison"
    if any(x in q for x in ["limitation", "weakness"]):
        return "limitation"
    if any(x in q for x in ["equation", "proof", "math"]):
        return "math"
    return "summary"


def build_metadata_filter(query_class: str, query: str) -> Dict:
    if query_class == "figure":
        return {"type": "image_reasoning"}
    if query_class == "method":
        return {"section": "method"}

    maybe_paper_id = None
    tokens = query.split()
    for token in tokens:
        if "v" in token and any(ch.isdigit() for ch in token):
            maybe_paper_id = token.strip(".,")
            break
    if maybe_paper_id:
        return {"paper_id": maybe_paper_id}

    return {}


def apply_metadata_filter(docs: List, metadata_filter: Dict):
    if not metadata_filter:
        return docs
    filtered = []
    for doc in docs:
        ok = True
        for key, value in metadata_filter.items():
            if doc.metadata.get(key) != value:
                ok = False
                break
        if ok:
            filtered.append(doc)
    return filtered
