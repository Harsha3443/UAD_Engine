from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "UAD Engine"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "mssql+aioodbc://@BLUEJADE\\SA/UnifiedApplicationDatabase?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()