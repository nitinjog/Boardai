from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./boardai.db"
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    UPLOAD_DIR: str = "./uploads"
    PDF_OUTPUT_DIR: str = "./generated_pdfs"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    MAX_UPLOAD_SIZE_MB: int = 10

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
