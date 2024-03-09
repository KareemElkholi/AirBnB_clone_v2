#!/usr/bin/python3
"""BaseModel class module"""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime


Base = declarative_base()


class BaseModel:
    """BaseModel class"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """constructor"""
        if kwargs:
            format = "%Y-%m-%dT%H:%M:%S.%f"
            for k, v in kwargs.items():
                if k in ["created_at", "updated_at"] and k != "__class__":
                    self.__dict__[k] = datetime.strptime(v, format)
                elif k != "__class__":
                    self.__dict__[k] = v
            if "id" not in kwargs:
                self.id = str(uuid4())
                self.created_at = self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """overrides __str__"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates updated_at with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__"""
        new_dict = {}
        new_dict["__class__"] = type(self).__name__
        for k, v in self.__dict__.items():
            if k in ["created_at", "updated_at"]:
                v = v.isoformat()
            elif k == "_sa_instance_state":
                continue
            new_dict[k] = v
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
