from celery import Celery
from app.core.config import get_settings

celery_app = Celery(
    "worker",
    broker=get_settings().redis_url,
    backend=get_settings().redis_url
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


_documents = {}


@celery_app.task(bind=True)
def process_document(self, task_id: str, file_content: bytes, filename: str, user_id: str = "default"):
    from app.services.document_processor import DocumentParser, ChunkProcessor
    from app.services.vector_store import VectorStore
    import uuid

    parser = DocumentParser()
    chunks_processor = ChunkProcessor(chunk_size=500, chunk_overlap=50)
    vector_store = VectorStore()

    documents = parser.parse(file_content, filename)
    chunks = chunks_processor.split(documents)

    document_id = str(uuid.uuid4())
    _documents[document_id] = {
        "id": document_id,
        "userId": user_id,
        "s3Key": f"documents/{user_id}/{document_id}/{filename}",
        "status": "completed",
        "metadata": {"filename": filename, "chunk_count": len(chunks)}
    }

    vector_store.upsert_vectors(chunks, user_id, document_id)

    return {"task_id": task_id, "document_id": document_id, "status": "completed", "chunks_processed": len(chunks)}


def process_document_sync(task_id: str, file_content: bytes, filename: str, user_id: str = "default"):
    from app.services.document_processor import DocumentParser, ChunkProcessor
    from app.services.vector_store import VectorStore
    import uuid

    parser = DocumentParser()
    chunks_processor = ChunkProcessor(chunk_size=500, chunk_overlap=50)
    vector_store = VectorStore()

    documents = parser.parse(file_content, filename)
    chunks = chunks_processor.split(documents)

    document_id = str(uuid.uuid4())
    _documents[document_id] = {
        "id": document_id,
        "userId": user_id,
        "s3Key": f"documents/{user_id}/{document_id}/{filename}",
        "status": "completed",
        "metadata": {"filename": filename, "chunk_count": len(chunks)}
    }

    vector_store.upsert_vectors(chunks, user_id, document_id)

    return {"task_id": task_id, "document_id": document_id, "status": "completed", "chunks_processed": len(chunks)}
