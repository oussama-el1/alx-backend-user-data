#!/usr/bin/env python3
"""
Hash Method
"""
import bcrypt
from db import DB
from user import User

from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> str:
    """
    :param pwd:
    :type pwd:
    :return:
    :rtype:
    """

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """  register_user  """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(email=email,
                                     hashed_password=_hash_password(password))
        return user