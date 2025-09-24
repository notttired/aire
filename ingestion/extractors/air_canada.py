from .base_extractor import BaseExtractor
from models.flight import FlightPrice, RoundTripFlightPrice
from typing import List

class BaseExtractor(BaseExtractor):

    async def extract_flight_price(self, html_content: str) -> List[FlightPrice | RoundTripFlightPrice]:
        pass