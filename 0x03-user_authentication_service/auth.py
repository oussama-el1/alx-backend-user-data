#!/usr/bin/env python3
"""
Hash Method
"""
import bcrypt


def _hash_password(password: str) -> str:
    """
    :param pwd:
    :type pwd:
    :return:
    :rtype:
    """

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed
