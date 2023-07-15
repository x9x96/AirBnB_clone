#!/usr/bin/python3
"""FileStorage class module"""
import json
import os
import datetime


class FileStorage:
    """
    A class for file storage and object serialization/deserialization.

    Attributes:
        __objects (dict): A dictionary to store serialized objects.
        __file_path (str): The path to the file used for storage.
    """

    __objects = {}
    __file_path = "file.json"

    def attributes(self):
        """
        Get the dictionary of class names and their attribute definitions.

        Returns:
            dict: A dictionary mapping class names to their
            attribute definitions.
        """

        attributes = {
            "BaseModel": {
                "id": str, "created_at": datetime.datetime,
                "updated_at": datetime.datetime
            },
            "User": {
                "email": str, "password": str,
                "first_name": str, "last_name": str
            },
            "State": {
                "name": str
            },
            "City": {
                "state_id": str, "name": str
            },
            "Amenity": {
                "name": str
            },
            "Place": {
                "city_id": str, "user_id": str, "name": str,
                "description": str, "number_rooms": int,
                "number_bathrooms": int, "max_guest": int,
                "price_by_night": int, "latitude": float,
                "longitude": float, "amenity_ids": list
            },
            "Review": {
                "place_id": str, "user_id": str,
                "text": str
            }
        }
        return attributes

    def classes(self):
        """
        Get the dictionary of class names and their corresponding classes.

        Returns:
            dict: A dictionary mapping class names to their classes.
        """

        from models.user import User
        from models.city import City
        from models.place import Place
        from models.state import State
        from models.review import Review
        from models.amenity import Amenity
        from models.base_model import BaseModel

        classes = {
            "BaseModel": BaseModel, "User": User,
            "State": State, "City": City,
            "Amenity": Amenity, "Place": Place,
            "Review": Review
        }
        return classes

    def reload(self):
        """
        Reload serialized objects from the file, if it exists.
        """

        if not os.path.isfile(self.__file_path):
            return
        with open(self.__file_path, "r", encoding="utf-8") as file:
            deserialized_dict = json.load(file)
            deserialized_dict = {key: self.classes()[value[
                "__class__"]](**value)
                                 for key, value in deserialized_dict.items()}
            self.__objects = deserialized_dict

    def new(self, obj):
        """
        Add a new object to the storage.

        Args:
            obj: The object to be added.
        """

        object_key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[object_key] = obj

    def all(self):
        """
        Get all serialized objects.

        Returns:
            dict: A dictionary of serialized objects.
        """

        return self.__objects

    def save(self):
        """
        Save the serialized objects to the file.
        """

        with open(self.__file_path, "w", encoding="utf-8") as file:
            objects_to_serialize = {
                key: value.to_dict() for key, value in self.__objects.items()}
            json.dump(objects_to_serialize, file)
