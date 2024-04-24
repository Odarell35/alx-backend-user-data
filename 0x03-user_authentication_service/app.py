#!/usr/bin/env python3
"""FLASK APP"""
from auth import Auth
from flask import Flask, jsonify, request,

app = Flask(__name__)
AUTH = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """returns message"""
    return jsonify({"message": "Bienvenue"}), 200

@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """register user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"messege": "email already registered"}), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
