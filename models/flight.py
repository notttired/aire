from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass(frozen=True)
class FlightRoute:
    origin: str
    destination: str

@dataclass(frozen=True)
class DateRange:
    start: datetime
    end: datetime

@dataclass(frozen=True)
class Flight:
    route: FlightRoute
    date_range: DateRange
    flight_number: str
    stops: Optional[List[str]] = field(default_factory=list)

@dataclass(frozen=True)
class RoundTripFlight:
    outbound: Flight
    inbound: Flight

@dataclass
class FlightPrice:
    flight: Flight
    price: float
    currency: str = "CAD"
    scraped_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class RoundTripFlightPrice:
    round_trip: RoundTripFlight
    price: float
    currency: str = "CAD"
    scraped_at: datetime = field(default_factory=datetime.utcnow)