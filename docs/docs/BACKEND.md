# Backend Structure (FastAPI)

- `/app/api/`: Endpoints for `chat`, `files`, `admin`.
- `/app/core/`: Security, Config, LLM configuration.
- `/app/services/`: LangChain wrappers, Pinecone helpers.
- `/app/tasks/`: Celery task definitions for asynchronous ingestion.