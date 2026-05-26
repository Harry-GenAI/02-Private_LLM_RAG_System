import os
import re
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# 1. Setup Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Preprocessing fun or Clean Text Function (Regex to fix PDF line breaks)
def clean_text(text):
    print("starting ingesting")
    # Replace single \n with space, but don't touch double \n\n
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    # Collapse multiple spaces into one
    text = re.sub(r' +', ' ', text)
    # 🔥 FIX: remove leading punctuation like ". "
    text = re.sub(r'^[\.\,\-\:]+\s*', '', text)
    return text.strip()

# 3. Load Documents
def load_docs(folder="docs"):
    documents = []

    if not os.path.exists(folder):
        print(f"Error: '{folder}' folder not found.")
        return []

    for file in os.listdir(folder):
        if not file.endswith(".pdf"):
            continue
            
        path = os.path.join(folder, file)
        loader = PyPDFLoader(path)
        docs = loader.load()

        # Apply cleaning and add your specific metadata
        for doc in docs:
            #doc.page_content = clean_text(doc.page_content)
            doc.metadata["source"] = file
            doc.metadata["doc_type"] = file.replace(".pdf", "")
            doc.metadata["department"] = "general"
        
        documents.extend(docs)
    return documents

# 4. Create Chunks (Using only RecursiveCharacterTextSplitter)
def create_chunks(docs):
    cleaned_docs = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", ".", " "]
    )
    chunks = splitter.split_documents(docs)

    for chunk in chunks:
      chunk.page_content = clean_text(chunk.page_content)
      cleaned_docs.append(chunk)
    return cleaned_docs

# 5. Build Chroma Vector DB
def build_vectordb(chunks):
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./chroma_db",
        collection_metadata={"hnsw:space": "cosine"}
    )
    vector_db.persist()
    return vector_db

# 6. Main
def main():
    #print("--- Starting Ingestion (Project II) ---")
    
    # Load and Clean
    documents = load_docs()
    
    # Chunk (Simple Recursive Splitter)
    chunks = create_chunks(documents)
    
    # Build Database
    # build_vectordb(chunks)
    
    for i, document in enumerate(documents):
        print(f"doc{i}\n {document}\n\n")
    #print(documents)

if __name__ == "__main__":
    main()