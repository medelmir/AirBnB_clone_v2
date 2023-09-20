#!/usr/bin/python3
"""
This module creates an instance of DBStorage and FileStorage, and allows
to change storage type directly by using an environment variable.
"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import os


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
