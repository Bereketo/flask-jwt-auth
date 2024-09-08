# Flask Authentication System

A comprehensive Flask-based authentication system using JWT tokens and MongoDB. This project includes user registration, login, token management (verification and refresh).

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## Project Overview

This project is a web application built with Flask that provides secure user authentication using JWT tokens. It includes endpoints for user registration, login, token verification, and token refreshing. Additionally, it features a profile page where users can manage their tokens.

## Features

- **User Registration**: Users can register with an email and password.
- **User Login**: Users can log in to receive a JWT token.
- **Token Management**: Users can verify and refresh their JWT tokens.
- **Profile Management**: Users can view and manage their tokens through a dedicated profile page.

## Technologies Used

- **Backend**: Flask, Flask-PyMongo, PyJWT
- **Database**: MongoDB Atlas
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Local development (can be adapted for deployment on platforms like Heroku)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/flask-authentication-system.git
   cd flask-authentication-system
    ```
2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables:**
   Create a .env file in the root directory with the following content:
   ```bash
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   MONGO_URI=your_mongodb_uri
   ```
5. **Run the Application:**
   ```bash
   flask run
   ```

## Configuration
- **SECRET_KEY:** A secret key for Flask session management.
- **JWT_SECRET_KEY:** A secret key used for encoding and decoding JWT tokens.
- **MONGO_URI:** The URI for connecting to your MongoDB database on Atlas or locally.

# Usage
- **Register:** Navigate to /register to create a new user.
- **Login:** Navigate to /login to authenticate and receive a JWT token.
- **Profile:** Navigate to /profile to view and manage your tokens.
- **Handle Token:** Navigate to /handle_token to fetch, verify, and refresh tokens.
