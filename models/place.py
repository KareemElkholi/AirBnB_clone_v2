#!/usr/bin/python3
"""Place class module"""
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import String, Integer, Float, Column, ForeignKey
from sqlalchemy.orm import relationship
import models


class Place(BaseModel, Base):
    """Place class"""
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="delete")

    @property
    def reviews(self):
        """getter attribute"""
        reviews = models.storage.all(Review).values()
        return [review for review in reviews if review.place_id == self.id]
