# Vector Strategy

- **Namespace:** Segregate vectors by `User_ID` to enforce data isolation.
- **Metadata:** Store `page_number`, `source_filename`, and `chunk_index` in Pinecone metadata to allow citations.
- **Search Strategy:** Hybrid search (Keyword + Dense Vector) for better retrieval accuracy on specific technical terms.