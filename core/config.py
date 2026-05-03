import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    embedding_dir: str = os.getenv("EMBEDDING_DIR", "data/embeddings")
    logs_dir: str = os.getenv("LOGS_DIR", "logs")
    prompt_version: str = os.getenv("PROMPT_VERSION", "v2")
    primary_llm: str = os.getenv("PRIMARY_LLM", "llama3.2")
    fallback_llm: str = os.getenv("FALLBACK_LLM", "mistral")
    llava_model: str = os.getenv("LLAVA_MODEL", "llava")
    embedding_model: str = os.getenv("EMBED_MODEL", "mxbai-embed-large")
    retriever_top_k: int = int(os.getenv("RETRIEVER_TOP_K", "8"))
    final_top_k: int = int(os.getenv("FINAL_TOP_K", "5"))
    query_timeout_s: int = int(os.getenv("QUERY_TIMEOUT_S", "60"))
    max_context_chars: int = int(os.getenv("MAX_CONTEXT_CHARS", "14000"))
    enable_pii_check: bool = _env_bool("ENABLE_PII_CHECK", True)
    api_key: str = os.getenv("RAG_API_KEY", "")


SETTINGS = Settings()
