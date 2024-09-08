from flask import Flask
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os

app = Flask(__name__)

mongo = PyMongo(app)
users_collection = mongo.db.users


class User:
    @staticmethod
    def create_user(name, email, password):
        hashed_password = generate_password_hash(password)
        user_id = users_collection.insert_one(
            {"name": name, "email": email, "password": hashed_password}
        ).inserted_id
        return str(user_id)

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return users_collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def check_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
