import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime
import json

class FlightDatabaseManager:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017")
        self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
        self.db = self.client["flights_db"]
        self.collection = self.db["flights"]

    def check_existing_flight(self, origin, destination, departure_time, price):
        """
        Check if a matching flight already exists in the database.
        Returns the existing flight document if found, None otherwise.
        """
        try:
            query = {
                "flight.route.origin": origin,
                "flight.route.destination": destination,
                "flight.date_range.start": departure_time,
                "price": price
            }

            existing_flight = self.collection.find_one(query)

            if existing_flight:
                existing_flight["_id"] = str(existing_flight["_id"])
                return existing_flight
            return None

        except OperationFailure as e:
            print(f"Database operation failed: {e}")
            return None
        except ConnectionFailure as e:
            print(f"Could not connect to server: {e}")
            return None

    def save_flight(self, flight_data):
        """
        Saves a flight document with server timestamp.
        Returns the inserted document ID if successful.
        """
        try:
            # Add database timestamp
            flight_data["db_created_at"] = datetime.utcnow()

            result = self.collection.insert_one(flight_data)
            return str(result.inserted_id)

        except OperationFailure as e:
            print(f"Database operation failed: {e}")
            return None
        except ConnectionFailure as e:
            print(f"Could not connect to server: {e}")
            return None


db_manager = FlightDatabaseManager()