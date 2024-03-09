#!/usr/bin/python3
"""State class module"""
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column
from models.base_model import BaseModel, Base
from models.city import City
import models


class State(BaseModel, Base):
    """State class"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref="state", cascade="delete")

    @property
    def cities(self):
        """getter attribute"""
        cities = models.storage.all(City).values()
        return [city for city in cities if city.state_id == self.id]
