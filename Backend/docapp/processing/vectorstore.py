# docapp/processing/vectorstore.py

import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
collection = client.get_or_create_collection("document_chunks")

def add_to_vectorstore(doc_id, chunks, embeddings):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[f"{doc_id}_chunk_{i}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"doc_id": str(doc_id), "chunk_index": i}]
        )

def similarity_search(query_embedding, top_k=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
