from dataclasses import dataclass
from typing import Optional

@dataclass
class ScrapeTask:
    airline: str
    route: FlightRoute
    outbound: DateRange
    inbound: Optional[DateRange] = None
    retries: int = 0
    proxy: Optional[str] = None