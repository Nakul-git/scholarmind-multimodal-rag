PROMPT_TEMPLATES = {
    "v1": """
You are a research assistant. Use only context. Cite [Chunk X].
Context:\n{context}\nQuestion:\n{question}\nAnswer:
""",
    "v2": """
You are a highly accurate research paper assistant.
Rules:
- Use ONLY provided context
- No hallucination
- Cite inline [Chunk X]
- Mention page if relevant
- If insufficient context, say so
- Separate explanation and evidence

Context:
{context}

Question:
{question}

Return format:
Explanation:
...
Evidence:
- [Chunk X] ...
""",
    "v3": """
You are a strict RAG verifier.
Ground answer only in context, cite each claim with [Chunk X], and flag uncertainty.
Context:\n{context}\nQuestion:\n{question}\nAnswer:
""",
}


def get_prompt(version: str, context: str, question: str) -> str:
    template = PROMPT_TEMPLATES.get(version, PROMPT_TEMPLATES["v2"])
    return template.format(context=context, question=question)
