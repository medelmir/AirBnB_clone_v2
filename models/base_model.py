#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
import os


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(
        String(60),
        primary_key=True,
        nullable=False,
        unique=True
    )
    created_at = Column(
        DATETIME,
        nullable=False,
        default=datetime.utcnow()
    )
    updated_at = Column(
        DATETIME,
        nullable=False,
        default=datetime.utcnow()
    )

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            for key, val in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        setattr(self, key, datetime.fromisoformat(val))
                    else:
                        setattr(self, key, val)
            if not hasattr(kwargs, 'id'):
                setattr(self, 'id', str(uuid.uuid4()))
            if not hasattr(kwargs, 'created_at'):
                setattr(self, 'created_at', datetime.now())
            if not hasattr(kwargs, 'updated_at'):
                setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key, val in self.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(val, datetime):
                    dictionary[key] = val.isoformat()
                else:
                    dictionary[key] = val
        dictionary['__class__'] = self.__class__.__name__
        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
