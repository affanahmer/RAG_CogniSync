from .ingestion import celery_app, process_document

__all__ = ["celery_app", "process_document"]
