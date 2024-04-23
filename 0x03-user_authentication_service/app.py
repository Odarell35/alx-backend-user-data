#!/usr/bin/env python3
"""FLASK APP"""
from auth import Auth
from flask import Flask, jsonify, request,

app = Flask(__name__)

@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """returns message"""
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
