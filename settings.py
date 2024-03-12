from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    switchbot_token: str
    switchbot_secret: str
    loglevel: str = "INFO"
