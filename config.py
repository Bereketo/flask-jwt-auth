import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    OAUTH_CREDENTIALS = {
        "google": {
            "client_id": "your_google_client_id",
            "client_secret": "your_google_client_secret",
        }
    }
