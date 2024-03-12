from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    switchbot_token: str
    switchbot_secret: str
    target_pubsub_topic_path: str
    loglevel: str = "INFO"

    @property
    def target_pubsub_gcp_project(self) -> str:
        return self.target_pubsub_topic_path.split("/")[1]
