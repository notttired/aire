from abc import ABC, abstractmethod
from models.flight import FlightPrice, RoundTripFlightPrice
from typing import List

class BaseExtractor(ABC):

    @abstractmethod
    async def extract_flight_price(self, html_content: str) -> List[FlightPrice | RoundTripFlightPrice]:
        pass