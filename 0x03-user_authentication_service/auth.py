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

    def register_user(self, email: str, password: str) -> User:
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
            if bcrypt.checkpw(password.encode('utf-8'),
                              hashed_password.encode('utf-8')):
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

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        get_user_from_session_id method
        takes a single session_id string argument
        returns the corresponding User or None
        """
        if session_id is None:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """
        destroy_session
        takes a single user_id integer argument
        returns None
        """
        try:
            avail_user = self._db.find_user_by(id=user_id)
            self._db.update_user(avail_user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        get_reset_password_token
        It take an email string argument
        returns a string.
        """
        try:
            avail_user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(avail_user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update_password method
        reset_token string argument
        and a password string argument
        returns None
        """
        try:
            avail_user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(avail_user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
