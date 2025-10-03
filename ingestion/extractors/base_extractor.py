from abc import ABC, abstractmethod
from models.flight import FlightPrice
from models.scrape_task import ScrapeRequest
from typing import List

class BaseExtractor(ABC):

    @abstractmethod
    async def extract_flight_price(self, request: ScrapeRequest, html_content: str) -> List[FlightPrice]:
        pass