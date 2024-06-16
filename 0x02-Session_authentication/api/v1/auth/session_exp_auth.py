#!/usr/bin/env python3
"""
Expiration
"""

from session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    class Expiration for a session
    """

    def __init__(self):
        """
        Constructor for the Child class
        """
        try:
            session_duration = int(os.environ.get("SESSION_DURATION", 0))
        except (TypeError, ValueError):
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """ Overload create_session methods """

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {"user_id": user_id,
                                                  "created_at": datetime.now()}

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ overload user_id_for_session_id """

        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        if self.session_duration <= 0:
            return session_data.get("user_id")

        if session_data.get("created_at") is None:
            return None

        experation_time = (session_data.get("created_at") +
                           timedelta(seconds=self.session_duration))

        if experation_time < datetime.now():
            return None
        else:
            return session_data.get("user_id")
