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
        Define which routes don't need authentication
        """

        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False

        tmp = path + '/' if path[-1] != '/' else path

        if tmp in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header function
        """

        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user function
        """

        return None
