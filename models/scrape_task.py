from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .flight import FlightRoute, DateRange

@dataclass
class ScrapeTask:
    airline: str
    route: FlightRoute
    outbound: DateRange
    inbound: Optional[DateRange] = None
    retries: int = 0
    proxy: Optional[str] = None

@dataclass(frozen=True)
class ScrapeRequest:
    airline: str
    route: FlightRoute
    outbound: datetime
    inbound: Optional[datetime] = None
    retries: int = 0
    proxy: Optional[str] = None