from dotenv import load_dotenv
import os

# Load environment from file specified by ENV_FILE or fallback
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(dotenv_path=env_file)

class Settings:
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    # DATABASE_URL = os.getenv("DATABASE_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    WKHTMLTOPDF_PATH = os.getenv("WKHTMLTOPDF_PATH", "/usr/bin/wkhtmltopdf")

settings = Settings()