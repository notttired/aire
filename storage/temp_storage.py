from typing import List
import os, json
from models.flight import FlightPrice
from datetime import datetime


def append_to_file(flight_prices: List[FlightPrice]) -> None:
    data = {}
    if os.path.exists("temp_data.json"):
        with open("temp_data.json", "r") as file:
            data = json.load(file)

    data[datetime.now().isoformat()] = [flight_price.model_dump() for flight_price in flight_prices]

    with open("temp_data.json", "w") as file:
        json.dump(data, file)