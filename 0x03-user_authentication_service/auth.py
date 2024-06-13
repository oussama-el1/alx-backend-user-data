#!/usr/bin/env python3
"""
Hash Method
"""
import bcrypt
from db import DB
from user import User
import uuid

from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """_hash_password
    """

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """ generate_uuid """

    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """  register_user  """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email=email,
                                     hashed_password=_hash_password(password))
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ Valid User Credentials """

        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email):
        """create_session
        """

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except Exception:
            return None
