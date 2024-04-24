#!/usr/bin/env python3
"""Hash Password"""

import bcrypt
from db import DB
from uuid import uuid4
from user import User
from bcrypt import hashpw, gensalt, checkpw
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """generate uuid

    Returns:
        str: representation of a new UUID
    """
    return str(uuid4())

def _hash_password(password: str) -> str:
    """Generate a salted hash of the input password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()


    def register_user(self,email: str, password: str) -> User:
        """ method to register user
            attr: email, password
            return user object itf avail
        """
        try:
            avail_user = self._db.find_user_by(email=email)
            if avail_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
           return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Try locating the user by email.
        If it matches return True. 
        In any other case, return False.
        """
        avail_user = self._db.find_user_by(email=email)
        if avail_user:
            hashed_password = avail_user.password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return True
        return False

    def create_session(self, email: str) -> str:
        """
        create session
        returns the session ID as a string
        """
        try:
            avail_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(avail_user.id, session_id=session_id)
        except NoResultFound:
            return

