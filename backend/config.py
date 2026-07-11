import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "ai_interview_secret_key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///interview.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
