#!/usr/bin/python3
"""
The BaseModel module
"""


import models
import uuid
from datetime import datetime
from json import JSONEncoder


class BaseModel:
    """The basemodel class"""

    def __init__(self, *args, **kwargs):
        """Class initializes the class"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                elif key == "__class__":
                    continue

                setattr(self, key, value)
        else:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.id = str(uuid.uuid4())
            models.storage.new(self)

    def save(self):
        """save new information in the class object"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """return dictionary representaton of the instance"""
        dictrep = {}
        for key, value in self.__dict__.items():
            dictrep[key] = value
            if isinstance(value, datetime):
                dictrep[key] = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
        dictrep["__class__"] = type(self).__name__
        return dictrep

    def __str__(self):
        """return the string representation of the class object"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)


class BaseModelEncoder(JSONEncoder):
    """JSON Encoder for BaseModel"""

    def default(self, o):
        """ default function"""
        if isinstance(o, BaseModel):
            return o.to_dict()
        return super().default(o)

