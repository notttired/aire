import re
from models.flight import *
from ingestion.constants.air_canada import *

from ingestion.scrapers.base_scraper import BaseScraper
from models.flight import FlightPrice
from models.scrape_task import ScrapeRequest

from playwright.async_api import Browser, Page, BrowserContext


# noinspection DuplicatedCode
class AirCanadaScraper(BaseScraper):
    def __init__(self, browser: Browser):
        super().__init__(browser)

    async def scrape_html_content(self, request: ScrapeRequest, context: BrowserContext) -> str:
        return await self.scrape_html_content_one_way(request, context)

    async def scrape_html_content_one_way(self, request: ScrapeRequest, context: BrowserContext) -> str:
        page = await context.new_page()
        await page.goto(BASE_URL)

        # Select trip type
        await page.click(TRIP_TYPE_SELECTOR)
        await page.click(ONE_WAY_TRIP_SELECTOR)

        # Fill in FlightRoute
        await page.click(DEPARTURE_LOCATION_SELECTOR)
        await page.type(DEPARTURE_FORM_SELECTOR, request.route.origin)
        await self.__safe_click(page, SEARCH_RESULT_SELECTOR_0)
        await page.click(ARRIVAL_LOCATION_SELECTOR)
        await page.type(ARRIVAL_FORM_SELECTOR, request.route.destination)
        await self.__safe_click(page, SEARCH_RESULT_SELECTOR_0)

        # Fill in time
        # Add logic for handling date not within shown window (need to click next)
        await page.click(DATE_SELECTOR)
        await page.locator(self.__date_to_locator(request.outbound)).first.click()
        await self.__safe_click(page, CONFIRM_DATES_SELECTOR)

        await page.click(SEARCH_BUTTON_SELECTOR)

        # Wait for results
        await page.wait_for_load_state("domcontentloaded", timeout=DEFAULT_TIMEOUT_MS)
        await page.wait_for_url(re.compile(rf"{NOT_FOUND_URL}|{ONE_WAY_FOUND_URL}"), timeout=DEFAULT_TIMEOUT_MS)
        await page.screenshot(path="page.png", full_page=True)
        content = await page.content()
        await context.close()
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

    async def __safe_click(self, page: Page, selector: str) -> bool:
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