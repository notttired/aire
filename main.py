from playwright.async_api import async_playwright
import asyncio

from ingestion.air_canada import air_canada_scraper
from ingestion.air_canada.air_canada_scraper import AirCanadaScraper
from models.scrape_task import ScrapeRequest
from models.flight import *


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        ac_scraper = AirCanadaScraper(browser)

        new_request = ScrapeRequest(
            airline = "AC",
            route = FlightRoute(
                "YYZ",
                "YYA"
            ),
            outbound = datetime(2025, 9, 25, 0, 0, 0),
            inbound = datetime(2025, 9, 28, 0, 0, 0),
        )

        await ac_scraper.scrape(new_request)

asyncio.run(main())