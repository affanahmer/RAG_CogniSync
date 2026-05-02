from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index: str
    database_url: str
    redis_url: str
    s3_bucket: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
