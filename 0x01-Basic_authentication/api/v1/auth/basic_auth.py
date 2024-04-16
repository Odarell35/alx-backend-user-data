#!/usr/bin/env python3
"""manage the API authentication"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """BasicAuth Class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """returns the Base64 part of the Authorization header"""
        if authorization_header is None or\
           type(authorization_header) is not str:
            return None
        hd = authorization_header.split(' ')

        return hd[1] if hd[0] == 'Basic' else None
