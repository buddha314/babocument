"""
Application Configuration

Loads configuration from environment variables using Pydantic Settings.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Babocument Server", alias="APP_NAME")
    environment: Literal["development", "staging", "production"] = Field(
        default="development", alias="ENVIRONMENT"
    )
    debug: bool = Field(default=True, alias="DEBUG")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", alias="LOG_LEVEL"
    )

    # LLM Configuration (Ollama)
    ollama_base_url: str = Field(
        default="http://localhost:11434", alias="OLLAMA_BASE_URL"
    )
    ollama_models: str = Field(default="d:/models", alias="OLLAMA_MODELS")
    llm_model: str = Field(default="ollama/llama3.2:3b", alias="LLM_MODEL")
    llm_temperature: float = Field(default=0.7, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=500, alias="LLM_MAX_TOKENS")
    llm_timeout: int = Field(default=30, alias="LLM_TIMEOUT")

    # Vector Database (ChromaDB)
    chroma_persist_directory: str = Field(
        default="./data/chroma", alias="CHROMA_PERSIST_DIRECTORY"
    )
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL"
    )
    
    # Document Storage
    document_storage_path: str = Field(
        default="./data/documents", alias="DOCUMENT_STORAGE_PATH"
    )

    # Redis (Event Bus & Caching)
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_password: str | None = Field(default=None, alias="REDIS_PASSWORD")

    # MCP Integration (Phase 2)
    biomcp_url: str | None = Field(default=None, alias="BIOMCP_URL")
    arxiv_mcp_url: str | None = Field(default=None, alias="ARXIV_MCP_URL")
    biorxiv_mcp_url: str | None = Field(default=None, alias="BIORXIV_MCP_URL")

    # Cloud API Fallbacks (Optional)
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    fallback_model: str | None = Field(default=None, alias="FALLBACK_MODEL")

    # CORS Settings
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        alias="CORS_ORIGINS",
    )

    @property
    def redis_url(self) -> str:
        """Construct Redis connection URL."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.

    Returns cached instance to avoid reloading from environment on every call.
    """
    return Settings()


# Convenience export
settings = get_settings()
