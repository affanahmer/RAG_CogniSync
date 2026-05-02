from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.api.files.schemas import UploadResponse, FileStatusResponse
from app.tasks.ingestion import process_document_sync
import uuid

router = APIRouter(prefix="/files", tags=["files"])

task_status = {}


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if file.size and file.size > 100 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 100MB)")

    allowed_extensions = {"pdf", "txt", "md", "docx"}
    ext = file.filename.lower().split(".")[-1]
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    task_id = str(uuid.uuid4())
    task_status[task_id] = {"status": "pending", "filename": file.filename}

    file_content = await file.read()
    task_status[task_id]["status"] = "processing"

    background_tasks.add_task(process_document_sync, task_id, file_content, file.filename)

    return UploadResponse(
        task_id=task_id,
        status="pending",
        filename=file.filename
    )


@router.get("/status/{task_id}", response_model=FileStatusResponse)
async def get_file_status(task_id: str):
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="Task not found")

    return FileStatusResponse(
        task_id=task_id,
        **task_status[task_id]
    )
