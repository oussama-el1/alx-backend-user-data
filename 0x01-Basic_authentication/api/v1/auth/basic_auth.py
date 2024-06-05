#!/usr/bin/env python3
"""
Basic auth module
"""
import base64
from api.v1.auth.auth import Auth


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
        return user_credentials[0], user_credentials[1]
