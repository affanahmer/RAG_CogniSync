from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    session_id: Optional[str] = None
    query: str


class QueryResponse(BaseModel):
    session_id: str
    response: str
    sources: list[dict]


class HistoryResponse(BaseModel):
    session_id: str
    messages: list[dict]
