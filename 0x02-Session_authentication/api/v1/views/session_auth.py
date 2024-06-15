#!/usr/bin/env python3
"""
view for Session Authentication
"""

from api.v1.views import app_views
from flask import request, jsonify
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_session():
    """ login_session """
    from models.user import User
    from api.v1.app import auth

    email = request.form.get("email")
    password = request.form.get("password")

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    selected_user = None
    for user in users:
        if user.is_valid_password(password):
            selected_user = user
    if selected_user is None:
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(selected_user.id)

    response = jsonify(selected_user.to_json())
    response.set_cookie(os.environ.get('SESSION_NAME'), session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    """
    from api.v1.app import auth

    deleted = auth.destroy_session(request)

    if not deleted:
        abort(404)

    return jsonify({}), 200
