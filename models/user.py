#!/usr/bin/python3
"""User class module"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column

class User(BaseModel, Base):
    """User class"""
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
