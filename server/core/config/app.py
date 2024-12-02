from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_DEBUG: bool
    HOST: str
    PORT: int
    ENVIRONMENT: str
    WORKER: int
    LISTING_NAME_ITEMS_SEPARATOR: str
    PICTURES_DIRECTORY: str
    NOT_IMPORTED_SHEETS_DIRECTORY: str
    IMPORTED_SHEETS_DIRECTORY: str
    PARENT_DIRECTORY_PROJECTS_MAIN_FILE: str
    SEARCH_QUERY_SEPARATOR: str
    REDIS_SCRAPER_BREAK_KEY: str
    model_config = SettingsConfigDict(
        env_file="../.env", extra="ignore", env_file_encoding="utf-8"
    )


AppConfig = AppSettings()
