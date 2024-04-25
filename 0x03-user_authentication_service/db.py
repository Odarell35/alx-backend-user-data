#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add user
            returns a User object"""
        if not email or not hashed_password:
            return
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Find user
        return user
        """
        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError()

        new_user = self._session.query(User).filter_by(**kwargs).first()
        if not new_user:
            raise NoResultFound
        return new_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update user """
        user_data = ['id', 'email', 'hashed_password',
                     'session_id', 'reset_token']
        update_user = self.find_user_by(id=user_id)

        for x, y in kwargs.items():
            if x not in user_data:
                raise ErrorValue
            setattr(update_user, x, y)

        self._session.commit()
        return None
