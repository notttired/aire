import logging
import asyncio
from datetime import datetime
from typing import Dict

from celery.signals import worker_process_init, worker_process_shutdown

from ingestion.extractors.air_canada_extractor import AirCanadaExtractor
from models.flight import DateRange, FlightRoute
from models.scrape_task import ScrapeRequest
from orchestration.browser_manager import BrowserManager
from orchestration.scraper_orchestrator import ScraperOrchestrator
from models.scrape_task import ScrapeTask
from celery_app import app

from util.conversions import scrape_request_from_json, scrape_request_to_json

logger = logging.getLogger(__name__)

# Module level -> Every celery worker process imports it
browser_manager = BrowserManager(browser_type="chromium", config={"headless": False})

@worker_process_init.connect
def init_browser(**kwargs):
    asyncio.get_event_loop().run_until_complete(browser_manager.start())
    logger.info("Browser started")

@worker_process_shutdown.connect
def shutdown_browser(**kwargs):
    asyncio.get_event_loop().run_until_complete(browser_manager.stop())
    logger.info("Browser stopped")

@app.task
def scrape(request: Dict):
    request = scrape_request_from_json(request)

    logger.info(f"Starting scrape task")

    browser = browser_manager.get_browser()
    orch = ScraperOrchestrator(browser)
    asyncio.get_event_loop().run_until_complete(orch.scrape_request(request))

@app.task
def schedule():
    logger.info("Started scheduling task")
    sample_req = ScrapeRequest(
        route=FlightRoute(
            origin="YYZ",
            destination="YYC"
        ),
        outbound=datetime(2025, 10, 18, 0, 0, 0)
    )
    requests = [sample_req]

    for req in requests:
        scrape.delay(scrape_request_to_json(req))

@app.task
def extract(req: dict):
    req = scrape_request_from_json(req)
    with open("./cache/air_canada.txt", "r", encoding="utf-8") as f:
        html_content = f.read()

    ac_extractor = AirCanadaExtractor()
    prices = ac_extractor.extract_flight_price(req, html_content)
    logger.info(f"Prices: {prices}")
    return prices

# celery -A celery_app:app worker --loglevel=INFO