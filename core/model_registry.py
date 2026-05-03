from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ModelSpec:
    name: str
    provider: str
    timeout_s: int = 60


class ModelRegistry:
    def __init__(self):
        self._models: Dict[str, ModelSpec] = {
            "llama3.2": ModelSpec(name="llama3.2", provider="ollama", timeout_s=60),
            "mistral": ModelSpec(name="mistral", provider="ollama", timeout_s=45),
            "llava": ModelSpec(name="llava", provider="ollama", timeout_s=90),
        }

    def get(self, model_name: str) -> ModelSpec:
        if model_name not in self._models:
            raise KeyError(f"Model not registered: {model_name}")
        return self._models[model_name]


MODEL_REGISTRY = ModelRegistry()
