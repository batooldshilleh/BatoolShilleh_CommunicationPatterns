import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://foodfast_user:securepassword@localhost:5433/foodfast_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
