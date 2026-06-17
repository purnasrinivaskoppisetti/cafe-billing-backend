from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    API_TOKEN: str

    API_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()