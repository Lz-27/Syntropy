from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Seguridad
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    # Base de datos
    DATABASE_URL: str = "sqlite:///./tgs_hub.db"

    # Archivos
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_MB: int = 100

    # Extensiones permitidas (separadas por coma en .env)
    ALLOWED_EXTENSIONS: str = "pdf,docx,pptx,xlsx,txt,csv,png,jpg,jpeg,webp,svg,py,java,js,ts,sql,zip,rar"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def allowed_extensions_set(self) -> set:
        return {ext.strip().lower() for ext in self.ALLOWED_EXTENSIONS.split(",")}

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    @property
    def max_file_bytes(self) -> int:
        return self.MAX_FILE_MB * 1024 * 1024


settings = Settings()
