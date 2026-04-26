#1) how to check properly split chunks
from ingest import load_docs, create_chunks

docs = load_docs()
chunks = create_chunks(docs)

for i, c in enumerate(chunks):
    print(f"\n--- Chunk {i} ---\n{c.page_content}")