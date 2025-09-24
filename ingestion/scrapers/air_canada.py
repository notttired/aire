import re
from models.flight import *
from ingestion.constants.air_canada import *

from ingestion.scrapers.base_scraper import BaseScraper
from models.flight import FlightPrice
from models.scrape_task import ScrapeRequest

from playwright.async_api import Browser, Page

class AirCanadaScraper(BaseScraper):
    def __init__(self, browser: Browser):
        super().__init__(browser)

    async def scrape_html_content(self, request: ScrapeRequest) -> str:
        context = await self.browser.new_context()
        page = await context.new_page()
        await page.goto(BASE_URL)

        # Fill in FlightRoute
        await page.click(DEPARTURE_LOCATION_SELECTOR)
        await page.type(DEPARTURE_FORM_SELECTOR, request.route.origin)
        await self.safe_click(page, SEARCH_RESULT_SELECTOR_0)
        await page.click(ARRIVAL_LOCATION_SELECTOR)
        await page.type(ARRIVAL_FORM_SELECTOR, request.route.destination)
        await self.safe_click(page, SEARCH_RESULT_SELECTOR_0)

        # Fill in time
        # Add logic for handling date not within shown window (need to click next)
        await page.click(DEPARTURE_DATE_SELECTOR)
        await page.locator(self.date_to_locator(request.outbound)).first.click()
        await page.locator(self.date_to_locator(request.inbound)).first.click()
        await page.click(CONFIRM_DATES_SELECTOR)

        await page.click(SEARCH_BUTTON_SELECTOR)

        # Wait for results
        await page.wait_for_url(re.compile(rf"{NOT_FOUND_URL}|{FOUND_URL}"))
        await page.screenshot(path = "page.png", full_page = True)
        content = await page.content()
        await context.close()
        return content

    def date_to_locator(self, date: datetime) -> str:
        """
        :param date: datetime
        :return: Playwright attribute selector for date for searching for flights
        """
        out = f'td[data-date="{date.day}"][data-month="{date.month}"][data-year="{date.year}"]'
        return out

    async def safe_click(self, page: Page, selector: str) -> bool:
        """
        Clicks if it appears within timeout
        :param page: Page
        :param selector: str Any selector
        :return: Success
        """
        locator = page.locator(selector)
        if await locator.is_visible(timeout=DEFAULT_TIMEOUT_MS):
            await locator.click()
            return True
        else:
            print("Button not found")
            return False