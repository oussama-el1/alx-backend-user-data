#!/usr/bin/env python3
"""
Hash Method
"""
import bcrypt
from db import DB
from user import User
import uuid
from typing import Union
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

    def create_session(self, email: str):
        """create_session
        """

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get_user_from_session_id
        """

        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id) -> None:
        """destroy_session
        """

        try:
            self._db.update_user(user_id=user_id, session_id=None)
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """get_reset_password_token
        """

        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user_id=user.id, reset_token=token)
            return token
        except Exception:
            raise ValueError("User Not found")

    def update_password(self, reset_token: str, password: str) -> None:
        """update_password
        """

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user_id=user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except Exception:
            raise ValueError("User Not Found")
