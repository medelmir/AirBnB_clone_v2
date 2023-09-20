#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import os


place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        primary_key=True,
        nullable=False
    ),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id'),
        primary_key=True,
        nullable=False
    )
)

"""
Defines a table for creating the many-to-many relationship between places
and amenities. Each row represents a link between a place and an amenity
indicating that a specific place has a particular amenity.

Columns:
- place_id: The id of the place associated with the amenity.
- amenity_id: The id of the amenity associated with the place.
"""


class Place(BaseModel, Base):
    """
    A place to stay

    Attributes:
        __tablename__ (str): The class place table name.
        city_id (str): The city id where the place is located.
        user_id (str): The user id.
        name (str): The name of the place.
        description (str): The description text of the place.
        number_rooms (int): The place rooms number.
        number_bathrooms (int): The place bathrooms number.
        max_guest (int): The maximum guest number.
        price_by_night (int): The price by night of the place.
        latitude (float): The place latitude location coordinate.
        longitude (float): The place longitude location coordinate.
    """
    __tablename__ = 'places'

    city_id = Column(
        String(60),
        ForeignKey('cities.id'),
        nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    user_id = Column(
        String(60),
        ForeignKey('users.id'),
        nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    name = Column(
        String(128),
        nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    description = Column(
        String(1024),
        nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    number_rooms = Column(
        Integer,
        nullable=False,
        default=0
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    number_bathrooms = Column(
        Integer,
        nullable=False,
        default=0
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    max_guest = Column(
        Integer,
        nullable=False,
        default=0
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    price_by_night = Column(
        Integer,
        nullable=False,
        default=0
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0
    latitude = Column(
        Float,
        nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0
    longitude = Column(
        Float,
        nullable=True
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else 0.0

    amenity_ids = []

    reviews = relationship(
        'Review',
        backref='Place',
        cascade="all, delete, delete-orphan"
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else None
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship(
            'Amenity',
            backref='place_amenities',
            secondary=place_amenity,
            viewonly=False
        )
    else:

        @property
        def reviews(self):
            """Returns the place reviews"""
            from models import storage
            place_reviews = []
            for val in storage.all(Review).values():
                if val.place.id == self.id:
                    place_reviews.append(val)
            return place_reviews

        @property
        def amenities(self):
            """Returns the place amenities"""
            from models import storage
            place_amenities = []
            for val in sotrage.all(Amenity).values():
                if val.id in self.amenity_ids:
                    place_amenities.append(val)
            return place_amenities

        @amenities.setter
        def amenities(self, value):
            """Sets and adds an amenity to the place"""
            if type(value) is Amenity:
                if value.id not in self.amenity_ids:
                    self.amenity_ids.append(value.id)
