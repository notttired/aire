import asyncio

from celery_app import app
from celery_config.base_tasks import ManagedTask
from orchestration.scraper_orchestrator import ScraperOrchestrator
from resource_management.browser_manager import BrowserManager
from util.conversions import scrape_request_from_json


@app.task(base=ManagedTask, bind=True, name="tasks.scrape")
def scrape(self, request_dict: dict):
    request = scrape_request_from_json(request_dict)

    async def run_scrape():
        """Refactor"""
        manager = BrowserManager()
        await manager.start()

        proxy = await self.proxy_mgr.acquire()

        try:
            browser = manager.get_browser()
            request.proxy = proxy

            orch = ScraperOrchestrator(browser=browser)
            return [value.model_dump_json() for value in await orch.scrape_request(request=request)]
        finally:
            await self.proxy_mgr.release(proxy)
            await manager.stop()

    return asyncio.run(run_scrape())
