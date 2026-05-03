from langchain_ollama import ChatOllama


def generate_multi_queries(user_question: str):
    """
    Uses llama3.2 to generate different search queries.
    """

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    prompt = f"""
You are helping improve retrieval for a research paper RAG system.

Original user question:
{user_question}

Generate 4 alternative search queries.
Make them useful for finding relevant chunks in research papers.

Return only the queries, one per line.
"""

    try:
        response = llm.invoke(prompt)
        text = response.content

        queries = [
            line.strip("- ").strip()
            for line in text.split("\n")
            if line.strip()
        ]

        queries = [user_question] + queries[:4]

        return queries

    except Exception:
        return [
            user_question,
            f"Explain {user_question}",
            f"Research paper discussion about {user_question}",
            f"Technical details about {user_question}"
        ]