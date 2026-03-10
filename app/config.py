from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Dify
    dify_api_key: str = ""
    dify_base_url: str = "https://api.dify.ai/v1"

    # WeChat
    wechat_appid: str = ""
    wechat_secret: str = ""

    # JWT
    jwt_secret: str = "change-me-in-production"

    # Database
    database_url: str = "sqlite:///openclaw_assistant.db"

    # Quota
    default_free_quota: int = 20
    exempt_openids: str = ""  # comma-separated openids that bypass quota

    model_config = {"env_file": ".env"}


settings = Settings()
