#!/usr/bin/env python3
"""Module of Users views"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users():
    """GET /api/v1/users - Return a list of all User objects JSON represented"""
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id):
    """GET /api/v1/users/:id - Return a User object JSON represented"""
    if user_id == 'me':
        if not request.current_user:
            abort(404)
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """DELETE /api/v1/users/:id - Delete a User"""
    user = User.get(user_id)
    if not user:
        abort(404)
    user.remove()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """POST /api/v1/users/ - Create a new User"""
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid JSON'}), 400

    user = User(**data)
    try:
        user.save()
    except Exception as e:
        return jsonify({'error': f'Can\'t create User: {str(e)}'}), 400

    return jsonify(user.to_json()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """PUT /api/v1/users/:id - Update a User"""
    user = User.get(user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    user.update(data)
    return jsonify(user.to_json()), 200
