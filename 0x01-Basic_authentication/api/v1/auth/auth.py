#!/usr/bin/env python3
"""
Authorization module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth function
        """

        return False

    def authorization_header(self, request=None) -> str:
        """
        authorization_header function
        """

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user function
        """

        return None
