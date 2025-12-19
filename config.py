"""
Configuration settings for AI Image Analyzer
Uses Pydantic BaseSettings for environment variable management
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # API Configuration
    GEMINI_API_KEY: Optional[str] = None
    DEMO_MODE: bool = True
    
    # Application Info
    APP_NAME: str = "AI Image Analyzer"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Analyze images using LangChain and Google Gemini AI"
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()
