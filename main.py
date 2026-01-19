import logging
from datetime import datetime
import asyncio

from celery.result import AsyncResult

from models.flight import FlightRoute
from models.scrape_task import ScrapeRequest
from orchestration.scraper_orchestrator import ScraperOrchestrator
from resource_management.browser_manager import BrowserManager
from util.conversions import scrape_request_to_json
from ingestion import *

async def run_sample_task():
    sample_req = ScrapeRequest(
        route=FlightRoute(
            origin="YYZ",
            destination="YYC"
        ),
        outbound=datetime(2026, 1, 20, 0, 0, 0)
    )

    browser_mgr = BrowserManager(config={"headless": True})
    await browser_mgr.start()
    browser = browser_mgr.get_browser()
    orch = ScraperOrchestrator(browser)
    prices = await orch.scrape_request(sample_req)
    print(prices)

def send_sample_task():
    from celery_config.tasks import scrape
    sample_req = ScrapeRequest(
        route=FlightRoute(
            origin="YYZ",
            destination="YYC"
        ),
        outbound=datetime(2026, 1, 20, 0, 0, 0)
    )

    t_id = scrape.delay(scrape_request_to_json(sample_req)).id
    res = AsyncResult(t_id)
    res = res.get(timeout=60000)
    print(res)

if __name__ == "__main__":
    send_sample_task()
    # logging.basicConfig(level=logging.INFO)
    #
    # asyncio.run(run_sample_task())