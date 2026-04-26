BLOCKED_TERMS = {
    "ignore previous instructions",
    "jailbreak",
    "system prompt",
}


def is_safe(message: str) -> bool:
    if not message or not message.strip():
        return False

    normalized = message.lower()
    return not any(term in normalized for term in BLOCKED_TERMS)
