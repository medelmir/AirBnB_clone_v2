#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class Amenity(BaseModel, base):
    """ An amenity class """
    __tablename__ = 'amenities'

    name = Column(
        String(128),
        nullable=False
    ) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
