from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    postgres_dsn: PostgresDsn = "postgres://test_user:test_user@localhost/AYU_CSE"
    session_expire_time: int = 86400


settings = Settings()
