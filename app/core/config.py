import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    MONGO_URL = os.getenv("MONGO_URL")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

    ACCESS_TOKEN_EXPIRE_SECONDS = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 3600)
    )

    REFRESH_TOKEN_EXPIRE_DAYS = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)
    )

    MAX_ACTIVE_SESSIONS = int(
        os.getenv("MAX_ACTIVE_SESSIONS", 3)
    )

    OTP_LENGTH = int(
        os.getenv("OTP_LENGTH", 4)
    )

    OTP_EXPIRE_MINUTES = int(
        os.getenv("OTP_EXPIRE_MINUTES", 5)
    )

    LOGIN_OTP_LENGTH = int(
        os.getenv("LOGIN_OTP_LENGTH", 6)
    )

    LOGIN_OTP_EXPIRE_MINUTES = int(
        os.getenv("LOGIN_OTP_EXPIRE_MINUTES", 5)
    )

    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_FROM = os.getenv("SMTP_FROM")


settings = Settings()