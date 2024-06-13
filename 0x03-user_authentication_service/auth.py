#!/usr/bin/env python3
"""
Hash Method
"""
import bcrypt
from bcrypt


def _hash_password(pwd: str) -> bytes:
    """
    :param pwd:
    :type pwd:
    :return:
    :rtype:
    """

    pwd_bytes = pwd.encode('utf-8')

    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
