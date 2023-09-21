#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """
    Represent a State class.

    Attributes:
        __tablename__ (str): The state class table name.
        name (str): The state class name.
    """
    __tablename__ = "states"

    name = Column(
        String(128),
        nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete, delete-orphan"
        )
    else:
        @property
        def cities(self):
            """
            Returns the list of City instances with state_id
            equals to the current State.id
            """
            from models import storage
            state_cities = []
            for val in storage.all(City).values():
                if val.state_id == self.id:
                    state_cities.append(val)
            return state_cities
