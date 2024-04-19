#!/usr/bin/env python3
"""Manage the API authentication"""
import base64
from typing import Optional, Tuple, TypeVar

from flask import request

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """BasicAuth Class"""

    @staticmethod
    def extract_base64_authorization_header(authorization_header: str) -> Optional[str]:
        """Return the Base64 part of the Authorization header"""
        if not authorization_header or not isinstance(authorization_header, str):
            return None
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'basic':
            return None
        return parts[1]

    @staticmethod
    def decode_base64_authorization_header(base64_authorization_header: str) -> Optional[str]:
        """Return the decoded value of a Base64 string"""
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except (binascii.Error, UnicodeDecodeError):
            return None

    @staticmethod
    def extract_user_credentials(decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
        """Return the user email and password from the Base64 decoded value"""
        if not decoded_base64_authorization_header or ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    @staticmethod
    def user_object_from_credentials(user_email: str, user_pwd: str) -> Optional[User]:
        """Return the User instance based on his email and password"""
        if not user_email or not user_pwd:
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> Optional[User]:
        """Overloads Auth and retrieves the User instance for a request"""
        try:
            authorization_header = self.authorization_header(request)
            base64_header = self.extract_base64_authorization_header(authorization_header)
            if not base64_header:
                return None
            decoded_header = self.decode_base64_authorization_header(base64_header)
            if not decoded_header:
                return None
            email, password = self.extract_user_credentials(decoded_header)
            if not email or not password:
                return None
            return self.user_object_from_credentials(email, password)
        except Exception:
            return None
