from dataclasses import dataclass, field
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class FlightRoute(BaseModel):
    origin: str
    destination: str

class DateRange(BaseModel):
    start: datetime
    end: datetime

class Flight(BaseModel):
    route: FlightRoute
    date_range: DateRange
    flight_number: Optional[str] = None # Later implement
    stops: Optional[List[str]] = field(default_factory=list)

class FlightPrice(BaseModel):
    flight: Flight
    price: float
    currency: str = "CAD"
    scraped_at: datetime = field(default_factory=datetime.utcnow)