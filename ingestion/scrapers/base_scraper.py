from abc import ABC, abstractmethod
from models.flight import FlightPrice, RoundTripFlightPrice
from models.scrape_task import ScrapeTask
from playwright.async_api import Browser

class BaseScraper(ABC):
    def __init__(self, browser: Browser):
        self.browser = browser

    @abstractmethod
    async def scrape(self, task: ScrapeTask) -> list[FlightPrice | RoundTripFlightPrice]:
        pass