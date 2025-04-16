# config.py

import os

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class Settings:
    PROJECT_NAME: str = "Smart Analytics as a Service"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "msme_analytics")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    REPORT_EMAIL_RECEIVER: str = os.getenv("REPORT_EMAIL_RECEIVER", "")


settings = Settings()
