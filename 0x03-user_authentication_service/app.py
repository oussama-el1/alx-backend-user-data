#!/usr/bin/env python3
"""
Flask app
"""
from typing import Tuple

from flask import Flask, jsonify, request, abort, Response, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def greating():
    """ route of the app """

    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ users register """
    try:
        email = request.form["email"]
        password = request.form["password"]
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'])
def login() -> Tuple[Response, int]:
    """login
    """

    try:
        email = request.form["email"]
        password = request.form["password"]
    except KeyError:
        abort(400)

    try:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response, 200
        else:
            abort(401)
    except Exception:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Logout
    """

    session_id = request.cookies.get('session_id', None)
    if session_id is None:
        abort(400)

    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect(url_for('greating'))
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
