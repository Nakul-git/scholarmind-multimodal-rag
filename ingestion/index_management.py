import os
import shutil
from datetime import datetime


EMBED_DIR = "data/embeddings"


def backup_index():
    if not os.path.exists(EMBED_DIR):
        return None
    dst = f"{EMBED_DIR}_backup_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    shutil.copytree(EMBED_DIR, dst)
    return dst


def clear_index():
    if os.path.exists(EMBED_DIR):
        shutil.rmtree(EMBED_DIR)


def index_health():
    return {
        "exists": os.path.exists(EMBED_DIR),
        "files": sum(len(files) for _, _, files in os.walk(EMBED_DIR)) if os.path.exists(EMBED_DIR) else 0,
    }
