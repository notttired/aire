from abc import ABC, abstractmethod
from models.flight import *

from ingestion.base_scraper import BaseScraper
from models.flight import FlightPrice
from models.scrape_task import ScrapeTask

from playwright.async_api import Browser, async_playwright

class AirCanadaScraper(BaseScraper):
    def __init__(self, browser: Browser):
        super().__init__(browser)

    async def scrape(self, task: ScrapeTask) -> list[FlightPrice | RoundTripFlightPrice]:
        context = await self.browser.new_context()
        page = await context.new_page()