from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "AgriSentry API"
    hf_repo_id: Optional[str] = None
    model_filename: str = "../models/best.pt" # Default points to models directory
    confidence_threshold: float = 0.25

    class Config:
        env_file = ".env"

settings = Settings()
