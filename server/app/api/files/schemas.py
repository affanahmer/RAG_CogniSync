from pydantic import BaseModel
from typing import Optional


class UploadResponse(BaseModel):
    task_id: str
    status: str
    filename: str


class FileStatusResponse(BaseModel):
    task_id: str
    status: str
    document_id: Optional[str] = None
    error: Optional[str] = None
