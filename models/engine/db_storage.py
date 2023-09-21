#!/usr/bin/python3
"""
Defines a SQL database storage engine, that encapsulates functionality for
interacting with a SQL database, including creating an SQLAlchemy engine
managing database sessions, and handling environment-specific configurations.
"""
import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place, place_amenity
from models.amenity import Amenity
from models.review import Review


class DBStorage():
    """
    Manages a SQL database storage engine for a web app.

    Attributes:
        __engine: An SQLAlchemy database engine instance.
        __session: An SQLAlchemy session object.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the SQL DBstorage engine.
        Sets up the SQLAlchemy engine based on environment variables.
        """
        mysql_user = os.getenv('HBNB_MYSQL_USER')
        mysql_password = os.getenv('HBNB_MYSQL_PWD')
        mysql_host = os.getenv('HBNB_MYSQL_HOST')
        mysql_database = os.getenv('HBNB_MYSQL_DB')
        env_var = os.getenv('HBNB_ENV')

        db_url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
            mysql_user, mysql_password, mysql_host, mysql_database
        )

        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if env_var == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieve instances of specified classes
        (or all classes if not specified) from the database
        and return them as a dictionary.
        """
        objs = dict()
        classes = (User, State, City, Amenity, Place, Review)
        if cls is None:
            for cls_model in classes:
                query = self.__session.query(cls_model)
                for value in query.all():
                    key = "{}.{}".format(value.__class__.__name__, value.id)
                    objs[key] = value
        else:
            query = self.__session.query(cls)
            for value in query.all():
                key = "{}.{}".format(value.__class__.__name__, value.id)
                objs[key] = value

        return objs

    def new(self, obj):
        """Adds the object to the current database session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the current database session"""
        if obj is not None:
            self.__session.query(
                type(obj)).filter(type(obj).id == obj.id).delete(
                synchronize_session=False
            )

    def reload(self):
        """Reloads the database session"""
        Base.metadata.create_all(self.__engine)
        session_fact = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_fact)()

    def close(self):
        """Closes the database engine session"""
        self.__session.close()
