# app/staff.py

class Staff:
    def __init__(self, name, phone_number, active=False):
        self.name = name
        self.phone_number = phone_number
        self.active = active  # Status to track if the staff member is active
