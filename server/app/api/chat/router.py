from fastapi import APIRouter, HTTPException
from app.api.chat.schemas import QueryRequest, QueryResponse, HistoryResponse
from app.services.vector_store import VectorStore
from app.services.llm import generate_response
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

_conversations = {}


@router.post("/query", response_model=QueryResponse)
async def query_chat(request: QueryRequest):
    user_id = "default"

    session_id = request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())

    try:
        vector_store = VectorStore()
        search_results = vector_store.hybrid_search(request.query, user_id, top_k=5)
    except Exception as e:
        logger.warning(f"Pinecone search failed: {e}")
        search_results = []

    context = "\n\n".join([
        f"[Source: {r['metadata'].get('source_filename', 'unknown')}, "
        f"Page {r['metadata'].get('page_number', '?')}, "
        f"Chunk {r['metadata'].get('chunk_index', '?')}]: {r['text']}"
        for r in search_results
    ]) if search_results else "No relevant context found."

    if session_id not in _conversations:
        _conversations[session_id] = {
            "id": session_id,
            "userId": user_id,
            "title": request.query[:50],
            "messages": []
        }

    _conversations[session_id]["messages"].append({
        "role": "USER",
        "content": request.query
    })

    try:
        response_text = generate_response(request.query, context)
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        response_text = f"I apologize, but I'm having trouble generating a response. Please ensure the OpenAI API key is properly configured. Error: {str(e)}"

    _conversations[session_id]["messages"].append({
        "role": "ASSISTANT",
        "content": response_text
    })

    return QueryResponse(
        session_id=session_id,
        response=response_text,
        sources=[{"filename": r["metadata"].get("source_filename"), "page": r["metadata"].get("page_number")} for r in search_results]
    )


@router.get("/history", response_model=HistoryResponse)
async def get_history(session_id: str):
    if session_id not in _conversations:
        raise HTTPException(status_code=404, detail="Session not found")

    return HistoryResponse(
        session_id=session_id,
        messages=_conversations[session_id]["messages"]
    )
