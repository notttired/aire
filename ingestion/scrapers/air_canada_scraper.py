import asyncio
import re
from models.flight import *
from ingestion.constants.air_canada import *

from ingestion.scrapers.base_scraper import BaseScraper
from models.flight import FlightPrice
from models.scrape_task import ScrapeRequest

from playwright.async_api import Browser, Page, BrowserContext
import logging
logger = logging.getLogger(__name__)

import traceback


async def get_text_safe_async(page, selector):
    """
    Asynchronously retrieves inner text or returns an empty string
    if the element is not present, bypassing long timeouts.
    """
    locator = page.locator(selector)

    if await locator.count() > 0:
        return await locator.inner_text()

    return ""

class AirCanadaScraper(BaseScraper):
    def __init__(self, browser: Browser):
        super().__init__(browser)

    async def scrape_html_content(self, request: ScrapeRequest, context: BrowserContext) -> str:
        return await self.scrape_html_content_one_way(request, context)

    import re
    import asyncio

    async def get_text_safe_async(page, selector):
        """Helper to return text or empty string without timing out."""
        target = page.locator(selector)
        if await target.count() > 0:
            return await target.inner_text()
        return ""

    async def scrape_html_content_one_way(self, request: ScrapeRequest, context: BrowserContext) -> str:
        page = await context.new_page()
        try:
            # Initial navigation - 'domcontentloaded' is enough for the initial shell
            await page.goto(BASE_URL, wait_until="domcontentloaded")
            logger.info("Starting to scrape")

            # 1. Select Trip Type
            # Ensure the selector is visible before clicking; avoid force=True if possible
            await page.wait_for_selector(TRIP_TYPE_SELECTOR, state="visible")
            await page.click(TRIP_TYPE_SELECTOR)

            await page.wait_for_selector(ONE_WAY_TRIP_SELECTOR, state="visible")
            await page.click(ONE_WAY_TRIP_SELECTOR)
            logger.info("Selected one way trip type")

            # 2. Extract current location state
            departure_text_selector = f"{DEPARTURE_LOCATION_SELECTOR} > div:first-child > p:first-child"
            arrival_text_selector = f"{ARRIVAL_LOCATION_SELECTOR} > div:first-child > p:first-child"

            # Concurrent execution for performance
            departure_text, arrival_text = await asyncio.gather(
                get_text_safe_async(page, departure_text_selector),
                get_text_safe_async(page, arrival_text_selector)
            )
            logger.info(f"Current UI State - Depart: {departure_text} Arrival: {arrival_text}")

            # 3. Handle Departure Input
            if request.route.origin != departure_text:
                await page.click(DEPARTURE_LOCATION_SELECTOR)
                await page.wait_for_selector(DEPARTURE_FORM_SELECTOR, state="visible")
                await page.fill(DEPARTURE_FORM_SELECTOR, request.route.origin)

                # Wait for the specific result entry to appear in the dropdown
                await page.wait_for_selector(SEARCH_RESULT_SELECTOR_0, state="visible")
                await self.__safe_click(page, SEARCH_RESULT_SELECTOR_0)

            # 4. Handle Arrival Input
            await page.click("#pillsContainerRef")  # Closes previous dropdown if open

            if request.route.destination != arrival_text:
                await page.click(ARRIVAL_LOCATION_SELECTOR)
                await page.wait_for_selector(ARRIVAL_FORM_SELECTOR, state="visible")
                await page.fill(ARRIVAL_FORM_SELECTOR, request.route.destination)

                await page.wait_for_selector(SEARCH_RESULT_SELECTOR_0, state="visible")
                await self.__safe_click(page, SEARCH_RESULT_SELECTOR_0)

            logger.info("Filled in flight route")

            # 5. Handle Date Selection
            await page.click(DATE_SELECTOR)

            date_locator = page.locator(self.__date_to_locator(request.outbound)).first
            # Explicitly wait for the specific date to render in the calendar
            await date_locator.wait_for(state="attached", timeout=DEFAULT_TIMEOUT_MS)
            await date_locator.click()

            await self.__safe_click(page, CONFIRM_DATES_SELECTOR)
            logger.info("Date confirmed. Executing search...")

            # 6. Execute Search and Wait for Redirection
            await self.__safe_click(page, SEARCH_BUTTON_SELECTOR)

            # Instead of waiting for a load state, we wait for the URL to match our result pattern
            # This is the most reliable way to confirm the search was submitted
            await page.wait_for_url(
                re.compile(rf"{NOT_FOUND_URL}|{ONE_WAY_FOUND_URL}"),
                timeout=DEFAULT_TIMEOUT_MS,
                wait_until="domcontentloaded"
            )

            content = await page.content()
            logger.info("Found flight route information")

        finally:
            await page.close()

        return content
    async def scrape_html_content_round_trip(self, request: ScrapeRequest) -> str:
        context = await self.browser.new_context()
        page = await context.new_page()
        await page.goto(BASE_URL)

        # Fill in FlightRoute
        await page.click(DEPARTURE_LOCATION_SELECTOR)
        await page.type(DEPARTURE_FORM_SELECTOR, request.route.origin)
        await self.__safe_click(page, SEARCH_RESULT_SELECTOR_0)
        await page.click(ARRIVAL_LOCATION_SELECTOR)
        await page.type(ARRIVAL_FORM_SELECTOR, request.route.destination)
        await self.__safe_click(page, SEARCH_RESULT_SELECTOR_0)

        # Fill in time
        # Add logic for handling date not within shown window (need to click next)
        await page.click(DEPARTURE_DATE_SELECTOR)
        await page.locator(self.__date_to_locator(request.outbound)).first.click()
        await page.locator(self.__date_to_locator(request.inbound)).first.click()
        await page.click(CONFIRM_DATES_SELECTOR)

        await page.click(SEARCH_BUTTON_SELECTOR)

        # Wait for results
        await page.wait_for_url(re.compile(rf"{NOT_FOUND_URL}|{FOUND_URL}"))
        await page.screenshot(path = "page.png", full_page = True)
        content = await page.content()
        await context.close()
        return content

    def __date_to_locator(self, date: datetime) -> str:
        """
        :param date: datetime
        :return: Playwright attribute selector for date for searching for flights
        """
        out = f'td[data-date="{date.day}"][data-month="{date.month}"][data-year="{date.year}"]'
        return out

    async def _safe_event(self, page: Page, selector: str, event: str):
        """
        Clicks if it is visible
        :param page: Page
        :param selector: str Any selector
        :param event: str Any event (click, check, ...)
        :return: Success
        """
        locator = page.locator(selector)
        try:
            if await locator.is_visible():
                await locator.dispatch_event(event)
            return True
        except Exception as e:
            logger.info(f"Not found: {selector}")
            logger.info(f"Exception: {e}")
            return False

    async def __safe_click(self, page: Page, selector: str) -> bool:
        """
        Clicks if it is visible
        :param page: Page
        :param selector: str Any selector
        :return: Success
        """
        locator = page.locator(selector)
        try:
            if await locator.is_visible():
                await locator.dispatch_event("click")
            return True
        except Exception as e:
            logger.info(f"Button not found: {selector}")
            logger.info(f"Exception: {e}")
            return False