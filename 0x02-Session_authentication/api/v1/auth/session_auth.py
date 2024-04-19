#!/usr/bin/env pyhton3
"""Create a class SessionAuth that inherits from Auth"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
  """ a class SessionAuth that inherits from Auth"""
  pass
