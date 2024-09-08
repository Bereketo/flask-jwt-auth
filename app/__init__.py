from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from dotenv import load_dotenv
import os


load_dotenv()

mongo = PyMongo()


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # Debug prints to verify
    print(f"Loaded MONGO_URI: {os.getenv('MONGO_URI')}")
    print(f"Loaded SECRET_KEY: {os.getenv('SECRET_KEY')}")
    print(f"Loaded JWT_SECRET_KEY: {os.getenv('JWT_SECRET_KEY')}")

    try:
        mongo.init_app(app)
        print("MongoDB connection initialized")
    except Exception as e:
        print(f"Error initializing MongoDB connection: {e}")

    from app.routes import register_routes

    register_routes(app)

    return app
