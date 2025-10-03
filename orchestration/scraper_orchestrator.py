from playwright.async_api import Browser
from typing import List

from models.flight import FlightPrice
from models.scrape_task import ScrapeRequest

from orchestration.airlines import AIRLINES
from storage.temp_storage import append_to_file


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

        context = await self.new_context(request.proxy)
        html_content = await scraper.scrape_html_content(request, context)
        scrape_prices: List[FlightPrice] = extractor.extract_flight_price(request, html_content)
        print(scrape_prices)
        append_to_file(scrape_prices)
        return scrape_prices

    async def new_context(self, proxy=None):
        return await self.browser.new_context(proxy=proxy)