# CogniSync - AI-First Knowledge Engine

A scalable, RAG-based document interaction platform designed for enterprise-grade knowledge management.

## Tech Stack
- **Frontend:** Next.js, Tailwind CSS, Framer Motion
- **Backend:** FastAPI (Python), Celery/Redis (Task Queue)
- **AI/LLM:** LangChain, OpenAI API (GPT-4o), Whisper
- **Vector DB:** Pinecone
- **Database:** PostgreSQL (Prisma ORM)

## Getting Started
1. Clone the repo.
2. Install dependencies: `npm install` (frontend) and `pip install -r requirements.txt` (backend).
3. Configure environment variables in `.env`.
4. Run `docker-compose up` to start the vector db and cache.