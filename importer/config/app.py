from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    LISTING_NAME_ITEMS_SEPARATOR: str
    PICTURES_DIRECTORY: str
    NOT_IMPORTED_SHEETS_DIRECTORY: str
    IMPORTED_SHEETS_DIRECTORY: str
    PARENT_DIRECTORY_PROJECTS_MAIN_FILE: str
    SEARCH_QUERY_SEPARATOR: str
    REDIS_IMPORTER_BREAK_KEY: str
    IMPORTER_TIME_OUT: int
    GOOGLE_MAP_ACTIVE_HOURS_END_ID: str
    NESHAN_ACTIVE_HOURS_END_ID: str
    MIKHAM_DEFAULT_ACCOUNT_USERNAME: str
    MIKHAM_DEFAULT_ACCOUNT_PASSWORD: str
    MIKHAM_PASSWORD_SUFFIX: str

    model_config = SettingsConfigDict(
        env_file="../.env", extra="ignore", env_file_encoding="utf-8"
    )


AppConfig = AppSettings()
