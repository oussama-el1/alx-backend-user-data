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
