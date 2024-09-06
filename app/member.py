# app/member.py

from app.car import Car

class Member:
    def __init__(self, name, house_number, cars=None, member_type="Member"):
        self.name = name
        self.house_number = house_number
        self.cars = cars if cars else []  # List of Car objects
        self.type = member_type  # "Member" or "Guest"

    def add_car(self, car):
        """Add a car to the member's car list"""
        self.cars.append(car)
