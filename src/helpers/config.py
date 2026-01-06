from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    # MongoDB connection URL and database name
    MONGODB_URL: str
    MONGODB_DATABASE: str

    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str
    COHERE_API_KEY: str = None

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    INPUT_DEFUALT_MAX_CHARACTERS: int = None
    GENERATION_DEFAULT_MAX_TOKENS: int = None
    GENERATION_DEFAULT_TEMPRATURE: float = None

    class Config:
        # Path to environment variables file
        env_file = "src/.env"


def get_settings():
    return Settings()
