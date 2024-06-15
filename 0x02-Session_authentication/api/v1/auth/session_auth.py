#!/usr/bin/env python3
"""
Class Session Auth
"""

from .auth import Auth
import uuid


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

        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        :param session_id:
        :type session_id:
        :return:
        :rtype:
        """

        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
