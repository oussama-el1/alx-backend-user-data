#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request, abort
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
def login():
    """login
    """

    try:
        email = request.form["email"]
        password = request.form["password"]
    except KeyError:
        abort(400)

    try:
        if AUTH.valid_login(email, password):
            AUTH.create_session(email)
        else:
            abort(401)
    except Exception:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
