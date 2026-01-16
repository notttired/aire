from typing import List
import os, json
from models.flight import FlightPrice
from datetime import datetime


def safe_append_to_file(prices):
    try:
        append_to_file(prices)
    except Exception as e:
        print(e)
        pass

def append_to_file(flight_prices: List[FlightPrice]) -> None:
    data = {}
    if os.path.exists("temp_data.json"):
        with open("temp_data.json", "r") as file:
            data = json.load(file)

    data[datetime.now().isoformat()] = [flight_price.model_dump_json() for flight_price in flight_prices]

    with open("temp_data.json", "w") as file:
        json.dump(data, file)

def format():
    with open("temp_data.json", "r") as file:
        data = json.load(file)

    with open("temp_data.json", "w") as file:
        json.dump(data, file, indent=4)

def parse_json():
    with open("temp_data.json", "r") as file:
        data = json.load(file)

if __name__ == "__main__":
    format()