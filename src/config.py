from pydantic_settings import BaseSettings
from functools import lru_cache
import os

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    app_name: str
    admin_email: str
    secret: str
    algorithm: str
    refresh_exp: int
    access_exp: int

    # ext API parameters
    CURRENCY_DATA_API_KEY: str

    # db parameters
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_DRIVER_SYNC: str
    DB_DRIVER_ASYNC: str

    POSTGRES_DB: str = 'postgres'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'admin'

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+{self.DB_DRIVER_ASYNC}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class ProductionSettings(Settings):
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")


class DevelopmentSettings(Settings):
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".dev.env")


class TestingSettings(Settings):
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".tests.env")


@lru_cache
def get_settings():
    mode = os.getenv("API_MODE")
    if mode in ("test", "testing"):
        return TestingSettings()
    if mode in ("dev", "development"):
        return DevelopmentSettings()
    if mode in ("prod", "production"):
        return ProductionSettings()
    return ProductionSettings()


settings = get_settings()
