from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from pydantic import Field
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))



class Settings(BaseSettings):
    db_host: str = Field(..., env="DB_HOST", exclude=True)
    db_name: str = Field(..., env="DB_NAME", description="The database name")
    db_user: str = Field(..., env="DB_USER", description="The database user")
    db_pass: str = Field(..., env="DB_PASS", exclude=True)
    db_port: int = Field(5432, env="DB_PORT", gt=0, le=65535, description="The database port")

    class Config:
        env_file = '.env' # Specifies the .env file to load variables from

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(f"Loaded settings: {self.dict()}")


@lru_cache()
def get_settings() -> Settings:
    return Settings()