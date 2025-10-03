from playwright.async_api import async_playwright, Browser
from typing import Dict, List

from models.flight import FlightPrice
from models.scrape_task import ScrapeRequest

# Airline Imports
from ingestion.scrapers.base_scraper import BaseScraper
from ingestion.extractors.base_extractor import BaseExtractor

from orchestration.airlines import AIRLINES
# from storage.temp_storage import append_to_file


class ScraperOrchestrator:
    def __init__(self, browser: Browser):
        self.browser = browser

    async def scrape_request(self, request: ScrapeRequest) -> List[FlightPrice]:
        """
        Single unit of task
        """
        airline = AIRLINES[request.airline]

        scraper = airline["scraper"](self.browser)
        extractor = airline["extractor"]()
        html_content = await scraper.scrape_html_content(request)
        scrape_prices: List[FlightPrice] = extractor.extract_flight_price(request, html_content)
        print(scrape_prices)
        # append_to_file(scrape_prices)
        return scrape_prices