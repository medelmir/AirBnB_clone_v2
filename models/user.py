#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class User(BaseModel, Base):
    """
    This class defines a user by various attributes

    Attributes:
        __tablename__ (str): The class users table name.
        email (str): The user class email.
        password (str): The user class password.
        first_name (str): The user class first name.
        last_name (str): The user class last name.
        places: Represent a relationship with the class Place.
        reviews: Represent a relationship with the class Review.
    """
    __tablename__ = 'users'

    email = Column(
        String(128),
        nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    password = Column(
        String(128),
        nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    first_name = Column(
        String(128),
        nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    last_name = Column(
        String(128),
        nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    places = relationship(
        'Place',
        backref='user',
        cascade="all, delete, delete-orphan"
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    reviews = relationship(
        'Review',
        backref='user',
        cascade="all, delete, delete-orphan"
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
