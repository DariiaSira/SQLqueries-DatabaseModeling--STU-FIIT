from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    DATABASE_HOST: str
    DATABASE_PORT: str  # = os.environ.get("DATABASE_PORT")
    DATABASE_NAME: str  # = os.environ.get("DATABASE_NAME")
    DATABASE_USER: str  # = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD: str  # = os.environ.get("DATABASE_PASSWORD")

settings = Settings()
