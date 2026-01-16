# def test_connection(page):
#     page.goto("https://www.aircanada.com/home/ca/en/aco/flights")
#     page.wait_for_load_state("networkidle")
#     page.wait_for_timeout(2000)
#     assert "air" in page.title()
from datetime import datetime

from celery_config.tasks import extract
from models.flight import FlightRoute
from models.scrape_task import ScrapeRequest
from util.conversions import scrape_request_to_json


def test_extraction():
    sample_req = ScrapeRequest(
        route=FlightRoute(
            origin="YYZ",
            destination="YYC"
        ),
        outbound=datetime(2025, 10, 18, 0, 0, 0)
    )
    res = extract.delay(scrape_request_to_json(sample_req))
    assert res is not None