#!/usr/bin/env python3
"""Hash Password"""

import bcrypt
from db import DB
from uuid import uuid4
from user import User
from bcrypt import hashpw, gensalt, checkpw
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound

def _hash_password(password: str) -> str:
        """Generate a salted hash of the input password"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
