#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class City(BaseModel, Base):
    """
    Represent a City class that inherits from Base.

    Attributes:
        __tablename__ (str): The class city table name.
        name (str): The class city name.
        state_id (int): The state in which the city located.
        places: Represent a relationship with the class Place
    """
    __tablename__ = "cities"

    name = Column(
        String(128),
        nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    state_id = Column(
        String(60),
        ForeignKey('states.id'),
        nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    places = relationship(
        'Place',
        backref='cities',
        cascade="all, delete, delete-orphan"
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
