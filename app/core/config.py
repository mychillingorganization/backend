from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Tất cả config đọc từ file .env.
    pydantic-settings tự động map tên biến .env -> thuộc tính class (case-insensitive).
    """

    model_config = SettingsConfigDict(
        env_file=".env",           # Đọc từ file .env ở root project
        env_file_encoding="utf-8",
        case_sensitive=False,      # APP_ENV hay app_env đều được
        extra="ignore",            # Bỏ qua biến .env không khai báo ở đây
    )

    # ── Application ──────────────────────────────────────────
    APP_ENV: str = Field(default="development")
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)

    # ── Database (SQL Server) ─────────────────────────────────
    # Format: mssql+aioodbc://user:pass@host:port/dbname?driver=ODBC+Driver+17+for+SQL+Server
    DATABASE_URL: str = Field(...)   # ... = bắt buộc, không có default

    # ── Google Service Account ────────────────────────────────
    GOOGLE_SERVICE_ACCOUNT_FILE: str = Field(default="credentials/service_account.json")
    GMAIL_SENDER_EMAIL: str = Field(...)

# Singleton instance — import và dùng ở khắp nơi
settings = Settings()