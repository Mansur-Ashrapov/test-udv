from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PASS: str = 'password'


settings = Settings()