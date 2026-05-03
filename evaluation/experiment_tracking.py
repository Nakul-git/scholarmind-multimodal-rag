import json
import os
from datetime import datetime


def log_experiment(name: str, config: dict, scores: dict):
    os.makedirs("logs/experiments", exist_ok=True)
    payload = {
        "name": name,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "config": config,
        "scores": scores,
    }
    out = os.path.join("logs/experiments", f"{name}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return out
