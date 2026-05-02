from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.files import router as files_router
from app.api.chat import router as chat_router
from app.api.admin import router as admin_router

app = FastAPI(title="CogniSync API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")