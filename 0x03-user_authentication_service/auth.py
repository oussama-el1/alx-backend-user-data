#!/usr/bin/env python3
"""
Hash Method
"""
import bcrypt


def _hash_password(pwd: str) -> str:
    """
    :param pwd:
    :type pwd:
    :return:
    :rtype:
    """

    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return hashed
