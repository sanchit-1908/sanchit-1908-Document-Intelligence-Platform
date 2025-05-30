# docapp/processing/rag.py
import os
from pathlib import Path
from typing import List
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
from docapp.processing.vectorstore import similarity_search

# --- Configuration ---
MODEL_PATH = "F:/INTERNSHALA/Ergosphere/DocumentIntelligence/Backend/Models/Phi-3.5-mini-instruct.Q6_K.gguf"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Initialize Models ---
def load_models():
    """Load LLM and embedding models with error handling"""
    try:
        # Local Phi-3.5-mini GGUF model
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )
        
        # Embedding model
        embedder = SentenceTransformer(EMBEDDING_MODEL)
        
        print("✅ Models loaded successfully")
        return llm, embedder
        
    except Exception as e:
        print(f"❌ Model loading failed: {str(e)}")
        raise

llm, embedder = load_models()

# --- RAG Pipeline ---
def answer_query(query: str, top_k: int = 5) -> str:
    """Enhanced RAG pipeline with better context handling"""
    try:
        # 1. Generate query embedding
        query_embedding = embedder.encode(query, convert_to_tensor=False)
        
        # 2. Retrieve relevant documents with debugging
        results = similarity_search(query_embedding, top_k=top_k)
        
        if not results or not results.get('documents'):
            return "Error: No relevant documents found."
            
        context_chunks = results['documents'][0]
        print(f"\n🔍 Retrieved {len(context_chunks)} context chunks:")
        for i, chunk in enumerate(context_chunks):
            print(f"\nChunk {i+1}:\n{chunk[:200]}...")  # Print first 200 chars of each chunk
            
        context = "\n\n--- DOCUMENT CHUNK ---\n".join(context_chunks)
        
        # 3. Enhanced prompt template
        prompt = f"""
        DOCUMENT CONTEXT:
        {context}
        
        INSTRUCTIONS:
        - Answer using ONLY the provided context
        - If unsure, say "The document doesn't contain this information"
        - Keep answers concise and factual
        
        QUESTION: {query}
        
        ANSWER:
        """
        
        # 4. Generate answer with stricter parameters
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful document assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            temperature=0.3,  # Lower for more factual responses
            repeat_penalty=1.1  # Reduce repetition
        )
        
        answer = response["choices"][0]["message"]["content"].strip()
        print(f"\n🤖 Generated Answer:\n{answer}")
        return answer
        
    except Exception as e:
        print(f"⚠️ RAG Error: {str(e)}")
        return f"Error processing your query: {str(e)}"

# --- Test Case ---
if __name__ == "__main__":
    test_query = "What are the key findings in this document?"
    print(f"\n🧪 Test Query: {test_query}")
    print(f"💡 Test Answer: {answer_query(test_query)}")