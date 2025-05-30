 embedder.encode(query, convert_to_tensor=False)
        
        # # 2. Retrieve relevant documents
        # results = similarity_search(query_embedding, top_k=top_k)
        # context = "\n".join(results['documents'][0])