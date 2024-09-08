from flask import (
    request,
    jsonify,
    make_response,
    render_template,
    redirect,
    url_for,
    current_app,
)
from datetime import datetime, timedelta
import jwt
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId


def register_routes(app):
    @app.route("/", methods=["GET"])
    def home():
        return render_template("home.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if mongo.db is None:
            return "MongoDB not initialized", 500

        if mongo.db.users.find_one({"email": email}):
            return render_template("register.html", error="User already exists")

        hashed_password = generate_password_hash(password)
        user_id = mongo.db.users.insert_one(
            {"name": name, "email": email, "password": hashed_password}
        ).inserted_id
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")

        email = request.form.get("email")
        password = request.form.get("password")

        user = mongo.db.users.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            token = jwt.encode(
                {
                    "user_id": str(user["_id"]),
                    "exp": datetime.utcnow() + timedelta(minutes=10),
                },
                current_app.config["JWT_SECRET_KEY"],
            )

            response = make_response(redirect(url_for("profile")))
            response.set_cookie("token", token, httponly=True)
            return response
        return render_template("login.html", error="Invalid credentials")

    @app.route("/profile", methods=["GET"])
    def profile():
        token = request.cookies.get("token")
        if not token:
            return redirect(url_for("login"))

        try:
            data = jwt.decode(
                token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
            )
            user = mongo.db.users.find_one({"_id": ObjectId(data["user_id"])})
            return render_template("profile.html", user=user)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", error="Token expired"))
        except jwt.InvalidTokenError:
            return redirect(url_for("login", error="Invalid token"))

    @app.route("/verify_token", methods=["POST"])
    def verify_token():
        token = request.cookies.get("token")
        try:
            data = jwt.decode(
                token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
            )
            return jsonify({"data": data})
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

    @app.route("/refresh_token", methods=["POST"])
    def refresh_token():
        token = request.cookies.get("token")
        try:
            data = jwt.decode(
                token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
            )
            new_token = jwt.encode(
                {
                    "user_id": data["user_id"],
                    "exp": datetime.utcnow() + timedelta(minutes=10),
                },
                current_app.config["JWT_SECRET_KEY"],
            )

            response = make_response(jsonify({"message": "Token refreshed"}))
            response.set_cookie("token", new_token, httponly=True)
            return response
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

    @app.route("/handle_token", methods=["GET"])
    def handle_token():
        return render_template("handle_token.html")

    @app.route("/get_token", methods=["GET"])
    def get_token():
        token = request.cookies.get("token")
        if token:
            return jsonify({"token": token})
        else:
            return jsonify({"error": "No token found"}), 400

    @app.route("/logout", methods=["POST"])
    def logout():
        response = redirect(url_for("login"))
        response.set_cookie("token", "", expires=0)
        return response
