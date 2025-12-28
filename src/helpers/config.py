from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
  APP_NAME: str 
  APP_VERSION: str
  OPENAI_API_KEY: str
  FILE_ALLOWED_TYPES:list
  FILE_MAX_SIZE:int
  FILE_DEFAULT_CHUNK_SIZE: int
  # MongoDB connection URL and database name
  MONGODB_URL: str
  MONGODB_DATABASE: str
  
  class Config:
    # Path to environment variables file
    env_file = "src/.env"


def get_settings() :
  return Settings()