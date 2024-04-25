#!/usr/bin/env python3
"""FLASK APP"""
from auth import Auth
from flask import Flask, jsonify, request, redirect

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

@app.route('/session', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login"""
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """
     respond to the DELETE /sessions route
    """
    session_id = request.cookies.get('session_id')
    avail_user = AUTH.get_user_from_session_id(session_id)
    if avail_user:
        AUTH.destroy_session(avail_user.id)
        return redirect('/')
    else:
        abort(403)

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """profile
    Returns a message
    """
    session_id = request.cookies.get('session_id')
    avail_user = AUTH.get_user_from_session_id(session_id)
    if avail_user:
        return jsonify({"email": avail_user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
