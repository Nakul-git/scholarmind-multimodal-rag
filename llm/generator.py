from langchain_ollama import ChatOllama

from core.config import SETTINGS
from core.model_registry import MODEL_REGISTRY


def generate_answer(prompt: str):
    """Generate answer with primary model and fallback model."""
    primary = MODEL_REGISTRY.get(SETTINGS.primary_llm)
    fallback = MODEL_REGISTRY.get(SETTINGS.fallback_llm)

    for model in [primary, fallback]:
        try:
            llm = ChatOllama(model=model.name, temperature=0)
            response = llm.invoke(prompt)
            text = response.content if hasattr(response, "content") else str(response)
            if text and text.strip():
                return text, model.name
        except Exception:
            continue

    return "I could not generate a reliable answer from the available models.", "none"
