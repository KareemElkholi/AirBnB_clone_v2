#!/usr/bin/python3
"""FileStorage class module"""
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from json import dump, load


class FileStorage:
    """FileStorage class"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        self.__objects[f"{type(obj).__name__}.{obj.id}"] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        with open(self.__file_path, "w") as file:
            new = {}
            for k, v in self.__objects.items():
                new[k] = v.to_dict()
            dump(new, file, indent=4)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r") as file:
                loaded = load(file)
                for k, v in loaded.items():
                    self.__objects[k] = eval(v["__class__"])(**v)
        except FileNotFoundError:
            pass
