# app/database.py

from pymongo import MongoClient

class Database:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="village_system"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_db(self):
        return self.db
