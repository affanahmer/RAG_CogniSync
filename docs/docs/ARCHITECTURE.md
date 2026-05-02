# System Architecture

## Components
1. **Ingestion Service:** Handles file upload, OCR, and validation.
2. **Preprocessing Pipeline:** Splits documents into semantic chunks using recursive character splitting.
3. **Embeddings Engine:** Converts chunks into vector representations (OpenAI text-embedding-3-small).
4. **Vector DB:** Pinecone indexes the vectors.
5. **Retrieval Layer:** Cosine similarity search to retrieve top-k context.
6. **Generation Layer:** Inject retrieved context into a system prompt for the LLM.