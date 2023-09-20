#!/usr/bin/python3
"""
This module defines a class to manage file storage for hbnb clone.
And ensures that any changes are saved to the storage file and reloads
the storage for future use.
"""
import os
import json
from importlib import import_module


class FileStorage:
    """
    This class manages storage of hbnb models in JSON format.

    Attributes:
        __file_path (str): The path to the JSON file used for data storage.
        __objects (dict): A dictionary containing all the objects in storage.
        classes (dict): A dictionary mapping class names to their
                        corresponding model classes.
    """
    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        """
        Initializes the FileStorage.
        """
        self.classes = {
            'BaseModel': import_module('models.base_model').BaseModel,
            'User': import_module('models.user').User,
            'State': import_module('models.state').State,
            'City': import_module('models.city').City,
            'Place': import_module('models.place').Place,
            'Amenity': import_module('models.amenity').Amenity,
            'Review': import_module('models.review').Review
        }

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        """
        if cls is None:
            return self.__objects
        else:
            objs_list = {}
            for key, val in self.__objects.items():
                if isinstance(val, cls):
                    objs_list[key] = val
            return objs_list

    def new(self, obj):
        """
        Adds a new object to storage dictionary.
        """
        self.__objects.update(
            {obj.to_dict()['__class__'] + '.' + obj.id: obj}
        )

    def save(self):
        """
        Saves objects to the storage file.
        """
        with open(FileStorage.__file_path, 'w') as f:
            temp_file = {}
            temp_file.update(FileStorage.__objects)
            for key, val in temp_file.items():
                temp_file[key] = val.to_dict()
            json.dump(temp_file, f)

    def reload(self):
        """
        Loads ojects from the storage file.
        """
        cls_instence = self.classes

        if os.path.isfile(self.__file_path):
            temp_file = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp_file = json.load(f)
                for key, val in temp_file.items():
                    self.all()[key] = cls_instence[val['__class__']](**val)

    def delete(self, obj=None):
        """
        Delete an object from the storage.
        """
        if obj is not None:
            key = obj.to_dict()['__class__'] + '.' + obj.id
            if key in self.__objects.keys():
                del self.__objects[key]

    def close(self):
        """
        Closes the file storage engine.
        """
        self.reload()
