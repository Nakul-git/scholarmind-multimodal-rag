from core.config import SETTINGS
from llm.prompt_versions import get_prompt


def build_final_prompt(question: str, docs, version: str | None = None):
    context_blocks = []
    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata
        block = (
            f"[Chunk {i}]\n"
            f"Title: {metadata.get('title')}\n"
            f"Page: {metadata.get('page')}\n"
            f"Type: {metadata.get('type')}\n"
            f"Section: {metadata.get('section')}\n"
            f"Image: {metadata.get('image_path')}\n\n"
            f"Content:\n{doc.page_content}"
        )
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)
    if len(context) > SETTINGS.max_context_chars:
        context = context[: SETTINGS.max_context_chars]

    selected = version or SETTINGS.prompt_version
    return get_prompt(selected, context=context, question=question)
