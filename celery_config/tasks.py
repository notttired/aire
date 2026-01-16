from celery_app import app
from celery_config.base_tasks import ManagedTask
from orchestration.scraper_orchestrator import ScraperOrchestrator
from util.conversions import scrape_request_from_json


@app.task(base=ManagedTask, bind=True, name="tasks.scrape")
def scrape(self, request_dict: dict):
    request = scrape_request_from_json(request_dict)

    async def run_scrape():
        if not self.browser_mgr.is_connected():
            await self.browser_mgr.start()

        proxy = await self.proxy_mgr.acquire()
        request.proxy = proxy

        try:
            orch = ScraperOrchestrator(self.browser_mgr.get_browser())
            flight_prices = await orch.scrape_request(request)
        finally:
            await self.proxy_mgr.release(proxy)

        return flight_prices

    return self.loop.run_until_complete(run_scrape())