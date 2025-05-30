"""
Configuration management for the application
"""
import os
from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://main.dlimtlzxpr8ax.amplifyapp.com/"
    ]
    
    # File Upload Configuration
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [".txt", ".docx"]
    
    # API Configuration
    api_timeout: int = 30  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Parse CORS origins from environment if provided
        cors_env = os.getenv("CORS_ORIGINS")
        if cors_env:
            self.cors_origins = [origin.strip() for origin in cors_env.split(",")]
        
        # Validate required settings
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()