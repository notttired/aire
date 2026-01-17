import asyncio

from playwright.async_api import Browser
from typing import List

from models.flight import FlightPrice
from models.scrape_task import ScrapeRequest

from orchestration.airlines import AIRLINES
from storage.temp_storage import append_to_file, safe_append_to_file
from playwright_stealth import Stealth

import logging
logger = logging.getLogger(__name__)

class ScraperOrchestrator:
    def __init__(self, browser: Browser):
        if browser is None:
            raise ValueError(f"Browser not passed into ScraperOrchestrator")
        self.browser = browser

    async def scrape_request(self, request: ScrapeRequest) -> List[FlightPrice]:
        """
        Single unit of task
        """

        logger.info(f"Scraping request {request}")
        airline = AIRLINES[request.airline]

        scraper = airline["scraper"](self.browser)
        extractor = airline["extractor"]()

        logger.info(f"Creating new context")
        context = await self.new_context(request.proxy)
        try:
            logger.info(f"Created new context")
            html_content = await scraper.scrape_html_content(request, context)
            logger.info(f"Scraped html content")
            scrape_prices: List[FlightPrice] = extractor.extract_flight_price(request, html_content)
            logger.info(scrape_prices)
            # safe_append_to_file(scrape_prices)
        finally:
            await context.close()
        return scrape_prices

    async def new_context(self, proxy=None):
        ctx = await asyncio.wait_for(
            self.browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", proxy=proxy),
            timeout=5.0
        )
        logger.info(f"Created new unfinished context")
        stealth = Stealth(init_scripts_only=True)
        await stealth.apply_stealth_async(ctx)
        return ctx