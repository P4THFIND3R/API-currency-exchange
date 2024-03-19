from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    admin_email: str
    secret: str
    algorithm: str
    refresh_exp: int
    access_exp: int

    # db parameters
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_DRIVER_SYNC: str
    DB_DRIVER_ASYNC: str

    # ext API parameters
    CURRENCY_DATA_API_KEY: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+{self.DB_DRIVER_ASYNC}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()
