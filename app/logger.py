# app/logger.py

from datetime import datetime

class Logger:
    def __init__(self, db):
        self.db = db
        self.logs_collection = self.db["logs"]

    def log_action(self, plate_number, owner, house_number, action, type, staff):
        log_entry = {
            "plate_number": plate_number,
            "owner": owner,
            "house_number": house_number,
            "action": action,  # 'check-in' or 'check-out'
            "type": type,  # 'Member' or 'Guest'
            "staff": staff,
            "timestamp": datetime.now()
        }
        self.logs_collection.insert_one(log_entry)
