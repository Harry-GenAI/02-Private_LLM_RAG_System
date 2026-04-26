def rewrite_query(message: str, history: str = "") -> str:
    message = message.strip()
    if not history:
        return message

    return (
        "Conversation history:\n"
        f"{history}\n\n"
        "Rewrite the latest user question as a standalone search query:\n"
        f"{message}"
    )
