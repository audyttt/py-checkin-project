# app/system.py

from app.member import Member
from app.car import Car
from app.staff import Staff

class System:
    def __init__(self, db):
        self.db = db
        # Define collections for both members and staff
        self.members_collection = self.db["members"]
        self.staff_collection = self.db["staff"]
        self.logs_collection = self.db["logs"]

    # --- Member Management ---
    def get_all_members(self):
        """Retrieve all members from the MongoDB collection."""
        members = []
        cursor = self.members_collection.find()
        for member_data in cursor:
            cars = [Car(car['brand'], car['plate_number']) for car in member_data['cars']]
            members.append(Member(
                name=member_data['name'],
                house_number=member_data['house_number'],
                cars=cars,
                member_type=member_data['type']
            ))
        return members

    def add_member(self, member):
        """Add a new member to the MongoDB collection."""
        member_data = {
            "name": member.name,
            "house_number": member.house_number,
            "cars": [{"brand": car.brand, "plate_number": car.plate_number} for car in member.cars],
            "type": member.type
        }
        self.members_collection.insert_one(member_data)

    def get_member_by_name(self, name):
        """Find a member by their name."""
        return self.members_collection.find_one({"name": name})

    def get_member_by_plate(self, plate_number):
        """Find a member by the car's license plate."""
        return self.members_collection.find_one({"cars.plate_number": plate_number})

    def update_member_cars(self, name, updated_cars):
        """Update a member's cars list."""
        self.members_collection.update_one({"name": name}, {"$set": {"cars": updated_cars}})

    def edit_member(self, plate_number, member):
        """Edit a member's details based on their car's plate number."""
        member_data = {
            "name": member.name,
            "house_number": member.house_number,
            "cars": [{"brand": car.brand, "plate_number": car.plate_number} for car in member.cars],
            "type": member.type
        }
        self.members_collection.update_one({"cars.plate_number": plate_number}, {"$set": member_data})

    def delete_member_by_name(self, name):
        """Delete a member by name."""
        self.members_collection.delete_one({"name": name})

    # --- Staff Management ---
    def get_all_staff(self):
        """Retrieve all staff members from the MongoDB collection."""
        staff_list = []
        cursor = self.staff_collection.find()
        for staff_data in cursor:
            staff_list.append(Staff(
                name=staff_data['name'],
                phone_number=staff_data['phone_number'],
                active=staff_data.get('active', False)  # Handle active status for staff
            ))
        return staff_list

    def set_active_staff(self, staff_name):
        """Set a staff member as active and deactivate others."""
        # Deactivate all staff members first
        self.staff_collection.update_many({}, {"$set": {"active": False}})

        # Activate the selected staff member
        self.staff_collection.update_one({"name": staff_name}, {"$set": {"active": True}})

    def add_staff(self, staff):
        """Add a new staff member to the MongoDB collection."""
        staff_data = {
            "name": staff.name,
            "phone_number": staff.phone_number,
            "active": staff.active
        }
        self.staff_collection.insert_one(staff_data)

    def get_staff_by_name(self, name):
        """Find a staff member by their name."""
        return self.staff_collection.find_one({"name": name})

    def update_staff(self, name, updated_data):
        """Update an existing staff member's information."""
        self.staff_collection.update_one({"name": name}, {"$set": updated_data})

    def set_active_staff(self, staff_name):
        """Set a staff member as active and deactivate others."""
        # Deactivate all staff members first
        self.staff_collection.update_many({}, {"$set": {"active": False}})
        # Activate the selected staff member
        self.staff_collection.update_one({"name": staff_name}, {"$set": {"active": True}})

    def get_active_staff(self):
        """Retrieve the currently active staff member."""
        return self.staff_collection.find_one({"active": True})

    def delete_staff_by_name(self, name):
        """Delete a staff member by name."""
        self.staff_collection.delete_one({"name": name})
        
        
    def is_car_checked_in(self, plate_number):
        """Check if the car is currently checked in."""
        log = self.logs_collection.find_one({"plate_number": plate_number, "action": "check-in", "status": "active"})
        return log is not None

    def get_last_action(self, plate_number):
        """Get the last action (check-in or check-out) for a car based on the logs."""
        log = self.logs_collection.find_one({"plate_number": plate_number}, sort=[("timestamp", -1)])  # Get the latest log
        if log:
            return log["action"]
        return None

    def get_last_log_for_guest(self, plate_number):
        """Retrieve the latest log entry for a non-member (Guest) by plate number."""
        return self.logs_collection.find_one({"plate_number": plate_number, "type": "Guest"}, sort=[("timestamp", -1)])

    def log_action(self, plate_number, owner, house_number, action, timestamp, car_type, staff):
        """Log the check-in or check-out action in the logs."""
        log_data = {
            "plate_number": plate_number,
            "owner": owner,
            "house_number": house_number,
            "action": action,
            "timestamp": timestamp,
            "type": car_type,
            "staff": staff,
            "status": "active" if action == "check-in" else "completed"
        }
        if action == "check-in":
            # Insert a new check-in log
            self.logs_collection.insert_one(log_data)
        else:
            # For check-out, update the log to mark the check-in as completed
            self.logs_collection.update_one({"plate_number": plate_number, "action": "check-in", "status": "active"}, {"$set": {"status": "completed"}})
            self.logs_collection.insert_one(log_data)
            
    def get_log_count(self):
        """Get the total count of logs."""
        return self.logs_collection.count_documents({})

    def get_logs_by_page(self, page, logs_per_page):
        """Get logs for a specific page."""
        skip = page * logs_per_page
        return list(self.logs_collection.find().sort("timestamp", -1).skip(skip).limit(logs_per_page))
            
