import re
from typing import Tuple


INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"reveal system prompt",
    r"bypass safety",
    r"act as developer",
]

PII_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",
    r"\b\d{10}\b",
    r"\b\d{12}\b",
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
]


def check_prompt_injection(text: str) -> Tuple[bool, str]:
    lowered = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            return False, f"Prompt injection pattern detected: {pattern}"
    return True, "ok"


def check_pii(text: str) -> Tuple[bool, str]:
    for pattern in PII_PATTERNS:
        if re.search(pattern, text):
            return False, "Potential PII detected"
    return True, "ok"


def validate_query(text: str) -> Tuple[bool, str]:
    if not text or not text.strip():
        return False, "Empty query"
    if len(text) > 4000:
        return False, "Query too long"
    return True, "ok"
