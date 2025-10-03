from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from models.flight import FlightRoute, DateRange

class ScrapeTask(BaseModel):
    route: FlightRoute
    outbound: DateRange
    inbound: Optional[DateRange] = None
    retries: int = 0
    proxy: Optional[str] = None

class ScrapeRequest(BaseModel):
    route: FlightRoute
    outbound: datetime
    airline: str = "AC"
    retries: int = 0
    proxy: Optional[dict] = None