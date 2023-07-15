#!/usr/bin/python3
"""BaseModel class module"""
import uuid
from models import storage
from datetime import datetime


class BaseModel:
    """Base model for other classes"""

    def to_dict(self):
        """
        Convert the BaseModel instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the class name, attributes,
            created_at, and updated_at.
        """

        dict_representation = self.__dict__.copy()
        dict_representation["__class__"] = self.__class__.__name__
        dict_representation["created_at"] = self.created_at.isoformat()
        dict_representation["updated_at"] = self.updated_at.isoformat()
        return dict_representation

    def save(self):
        """
        Update the updated_at attribute to the current
        timestamp and save the instance.

        Returns:
            None
        """

        self.updated_at = datetime.today()
        storage.save()

    def __str__(self):
        """
        Return a string representation of the BaseModel instance.

        Returns:
            str: A formatted string containing the class name,
            id, and attributes.
        """

        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def __init__(self, *args, **kwargs):
        """
        Initialize a new instance of the BaseModel class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """

        if kwargs:
            for key, value in kwargs.items():
                if key in ("updated_at", "created_at"):
                    kwargs[key] = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f")
            self.__dict__ = kwargs
        else:
            self.id = str(uuid.uuid4())
            current_time = datetime.today()
            self.created_at = current_time
            self.updated_at = current_time
            storage.new(self)
