#!/usr/bin/python3
"""Place class module"""
from models.base_model import BaseModel


class Place(BaseModel):
    """Place class objects"""

    number_rooms = number_bathrooms = max_guest = price_by_night = 0
    latitude = longitude = 0.0
    city_id = user_id = name = description = ""
    amenity_ids = []
