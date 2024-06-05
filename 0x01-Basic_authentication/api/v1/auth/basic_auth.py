#!/usr/bin/env python3
"""
Basic auth module
"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class
    """

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """_summary_

        Args:
            authorization_header (str): _description_

        Returns:
            str: _description_
        """
        tmp = auth_header

        if tmp is None or not isinstance(tmp, str) or tmp[:6] != 'Basic ':
            return None

        return auth_header[6:]

    def decode_base64_authorization_header(self, b_64: str) -> str:
        """_summary_

        Args:
            base64_auth_header (str): _description_

        Returns:
            str: _description_
        """

        if b_64 is None or not isinstance(b_64, str):
            return None

        try:
            b64 = base64.b64decode(b_64)
            b64_decode = b64.decode('utf-8')
        except Exception:
            return None
        return b64_decode

    def extract_user_credentials(self, decode_b_64: str) -> (str, str):
        """_summary_

        Args:
            self (_type_): _description_
            str (_type_): _description_
        """

        if decode_b_64 is None or not isinstance(decode_b_64, str):
            return None, None
        if ':' not in decode_b_64:
            return None, None
        user_credentials = decode_b_64.split(':')
        if len(user_credentials) != 2:
            pwd = ':'.join(user_credentials[1:])
        else:
            pwd = user_credentials[1]
        return user_credentials[0], pwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """_summary_

        Args:
            self (_type_): _description_
        """

        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_
        """

        auth_header = self.authorization_header(request)
        b_64 = self.extract_base64_authorization_header(auth_header)
        decode_b_64 = self.decode_base64_authorization_header(b_64)
        user_email, user_pwd = self.extract_user_credentials(decode_b_64)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
