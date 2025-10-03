from abc import ABC, abstractmethod
from models.flight import FlightPrice
from models.scrape_task import ScrapeRequest
from playwright.async_api import Browser, BrowserContext


class BaseScraper(ABC):
    def __init__(self, browser: Browser):
        self.browser = browser

    @abstractmethod
    async def scrape_html_content(self, request: ScrapeRequest, context: BrowserContext) -> str:
        pass