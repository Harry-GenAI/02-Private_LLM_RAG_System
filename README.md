# Private LLM RAG System

A FastAPI-based private RAG application that ingests PDF documents, stores embeddings in a local Chroma vector database, retrieves relevant context, and generates answers with a locally saved Hugging Face causal language model.

## Project Structure

- `main.py` - FastAPI app and `/chat` endpoint.
- `main1.py` - CLI-style local test runner.
- `ingest.py` - PDF loading, text cleaning, chunking, and Chroma index creation.
- `rag.py` - Retrieval, reranking, and context compression.
- `llmservice.py` - Local model loading and response generation.
- `db.py` - PostgreSQL chat history storage.
- `docs/` - Source documents used for ingestion.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` from `.env.example` and fill in your private values.
4. Download/save the local model:

   ```bash
   python save_model.py
   ```

5. Build the vector index:

   ```bash
   python ingest.py
   ```

6. Run the API:

   ```bash
   uvicorn main:app --reload
   ```

## Notes

The following are intentionally ignored by Git because they are private, generated, or too large for a normal repository:

- `.env`
- `venv/`
- `local_model/`
- `chroma_db/`
- `faiss_index/`
- `__pycache__/`
