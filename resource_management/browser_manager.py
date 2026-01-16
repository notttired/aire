from playwright.async_api import async_playwright

class BrowserManager:
    def __init__(self, browser_type: str ="firefox", config: dict = None):
        self.browser_type = browser_type
        self.config = config or {}
        self.playwright = None
        self.browser = None

    async def start(self):
        self.playwright = await async_playwright().start()
        browser_cls = getattr(self.playwright, self.browser_type)
        self.browser = await browser_cls.launch(**self.config)
        return self.browser

    def is_connected(self):
        if not self.browser:
            return False
        return self.browser.is_connected()

    async def stop(self):
        if self.browser.is_connected():
            await self.browser.close()
            await self.playwright.stop()

    def get_browser(self):
        return self.browser