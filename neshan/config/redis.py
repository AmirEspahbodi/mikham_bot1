from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    REDIS_SLEEP_NESHAN_SEARCH_QUERIES: str
    REDIS_NESHAN_IN_PROCESSING_SEARCH_QUERY: str
    REDIS_HOST: str
    REDIS_PORT: int
    model_config = SettingsConfigDict(
        env_file="../.env", extra="ignore", env_file_encoding="utf-8"
    )


RedisConfig = RedisSettings()
