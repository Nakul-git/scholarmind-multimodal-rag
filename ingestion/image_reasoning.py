import hashlib
import os

import ollama

from core.cache import JsonDiskCache
from core.config import SETTINGS


LLAVA_CACHE = JsonDiskCache("data/cache/llava")


def _file_md5(path: str) -> str:
    md5 = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            md5.update(chunk)
    return md5.hexdigest()


def analyze_image_with_llava(image_path: str) -> str:
    if not os.path.exists(image_path):
        return ""

    image_hash = _file_md5(image_path)
    cached = LLAVA_CACHE.get(image_hash)
    if cached and cached.get("summary"):
        return cached["summary"]

    prompt = """
You are analyzing a figure, chart, table, architecture diagram, or visual from a research paper.
Describe: what it shows, labels/components, visible text, why important, concise searchable summary.
Do not hallucinate; mark unclear parts as unclear.
"""

    try:
        response = ollama.chat(
            model=SETTINGS.llava_model,
            messages=[{"role": "user", "content": prompt, "images": [image_path]}],
        )
        summary = response["message"]["content"]
        LLAVA_CACHE.set(image_hash, {"summary": summary, "image_path": image_path})
        return summary
    except Exception as e:
        print(f"LLaVA failed on image {image_path}: {e}")
        return ""
