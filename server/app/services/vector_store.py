from pinecone import Pinecone
from openai import OpenAI
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        self.settings = get_settings()
        self.pc = None
        self.index = None
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        self._initialized = False
        self._init_pinecone()

    def _init_pinecone(self):
        try:
            self.pc = Pinecone(api_key=self.settings.pinecone_api_key)
            self.index = self.pc.Index(self.settings.pinecone_index)
            self._initialized = True
        except Exception as e:
            logger.warning(f"Failed to initialize Pinecone: {e}")
            self._initialized = False

    def _embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def upsert_vectors(
        self,
        chunks: list[dict],
        user_id: str,
        document_id: str
    ) -> list[str]:
        if not self._initialized:
            logger.warning("Pinecone not initialized, skipping upsert")
            return []

        vector_ids = []
        for i, chunk in enumerate(chunks):
            text = chunk["page_content"]
            metadata = chunk.get("metadata", {})
            metadata["user_id"] = user_id
            metadata["document_id"] = document_id

            try:
                embedding = self._embed(text)
                vector_id = f"{document_id}-{i}"

                self.index.upsert(
                    vectors=[{
                        "id": vector_id,
                        "values": embedding,
                        "metadata": {
                            "text": text[:1000],
                            **metadata
                        }
                    }],
                    namespace=user_id
                )
                vector_ids.append(vector_id)
            except Exception as e:
                logger.error(f"Failed to upsert vector: {e}")

        return vector_ids

    def hybrid_search(
        self,
        query: str,
        user_id: str,
        top_k: int = 5
    ) -> list[dict]:
        if not self._initialized:
            logger.warning("Pinecone not initialized, returning empty results")
            return []

        try:
            query_embedding = self._embed(query)

            search_results = self.index.query(
                vector=query_embedding,
                namespace=user_id,
                top_k=top_k,
                include_metadata=True
            )

            return [
                {
                    "id": match["id"],
                    "score": match.get("score", 0),
                    "text": match["metadata"].get("text", ""),
                    "metadata": match["metadata"]
                }
                for match in search_results.get("matches", [])
            ]
        except Exception as e:
            logger.error(f"Pinecone search failed: {e}")
            return []
