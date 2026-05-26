
def build_prompt(context: str, question: str) -> str:
    return f"""You are a private RAG assistant. Answer only from the provided context.
If the context does not contain the answer, say you do not know.

Context:
{context}

Question:
{question}

Answer:"""
