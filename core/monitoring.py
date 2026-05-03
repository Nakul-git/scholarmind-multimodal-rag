import json
import os
import time
from contextlib import contextmanager
from typing import Dict


class PipelineMonitor:
    def __init__(self):
        self.step_times: Dict[str, float] = {}
        self.counters: Dict[str, float] = {
            "errors": 0,
            "retrieval_failures": 0,
            "empty_responses": 0,
            "token_estimate": 0,
            "cost_estimate_usd": 0,
        }

    @contextmanager
    def step(self, name: str):
        start = time.perf_counter()
        try:
            yield
        except Exception:
            self.counters["errors"] += 1
            raise
        finally:
            self.step_times[name] = self.step_times.get(name, 0.0) + (time.perf_counter() - start)

    def save(self, logs_dir: str):
        os.makedirs(logs_dir, exist_ok=True)
        with open(os.path.join(logs_dir, "latency_metrics.json"), "w", encoding="utf-8") as f:
            json.dump({"step_seconds": self.step_times, "counters": self.counters}, f, indent=2)
