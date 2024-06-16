#!/usr/bin/env python3
""" SessionDBAuth class
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import timedelta, datetime


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth database class"""

    def create_session(self, user_id=None):
        """
        :param user_id:
        :type user_id:
        :return:
        :rtype:
        """

        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            user_session.save_to_file()
        else:
            return None

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        :param session_id:
        :type session_id:
        :return:
        :rtype:
        """

        if session_id is None:
            return None

        users = UserSession.search({"session_id": session_id})
        if not users:
            return None

        user = users[0]

        expired_time = user.created_at + timedelta(seconds=self.session_duration)

        if expired_time < datetime.utcnow():
            return None

        return user.user_id

    def destroy_session(self, request=None):
        """Remove Session from Database"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        user_session = UserSession.search({
            'session_id': session_id
        })

        if not user_session:
            return False

        user_session = user_session[0]

        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
