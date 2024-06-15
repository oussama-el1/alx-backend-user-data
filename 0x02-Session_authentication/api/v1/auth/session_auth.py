#!/usr/bin/env python3
"""
Class Session Auth
"""

from .auth import Auth
import uuid
import os


class SessionAuth(Auth):
    """
    SessionAuth Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        :param user_id:
        :type user_id:
        :return:
        :rtype:
        """

        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""

        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """ Returns the session_cookie for a Request """

        if request is None:
            return None

        coockie_name = os.environ.get("SESSION_NAME")

        if coockie_name:
            return request.coockies.get(coockie_name)

        return None
