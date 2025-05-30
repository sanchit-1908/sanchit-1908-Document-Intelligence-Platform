import os
from .parser import extract_text
from .chunker import chunk_text
from .embedder import generate_embeddings
from .vectorstore import add_to_vectorstore

def process_document(document_obj):

    print("process_document function is entered")
    file_path = document_obj.file_path.path

    # 1. Extract text
    text = extract_text(file_path)

    # 2. Chunk the text
    chunks = chunk_text(text)

    # 3. Generate embeddings
    embeddings = generate_embeddings(chunks)

    # 4. Store in vector database
    add_to_vectorstore(document_obj.id, chunks, embeddings)

    return True
