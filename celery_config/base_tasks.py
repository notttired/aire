import asyncio
import celery
from resource_management.browser_manager import BrowserManager
from resource_management.proxy_manager import ProxyManager

import logging
logger = logging.getLogger(__name__)

class ManagedTask(celery.Task):
    """
    Manages the lifecycle of heavy resources like browsers and proxies
    """
    _browser_mgr: BrowserManager = None
    _proxy_mgr: ProxyManager = None
    _loop = None

    @property
    def browser_mgr(self):
        if self._browser_mgr is None:
            self._browser_mgr = BrowserManager(browser_type="firefox")
            logger.info("Initialized browser")
        return self._browser_mgr

    @property
    def proxy_mgr(self):
        if self._proxy_mgr is None:
            self._proxy_mgr = ProxyManager([])
            logger.info("Initialized proxy manager")
        return self._proxy_mgr

    @property
    def loop(self):
        if self._loop is None:
            self._loop = asyncio.new_event_loop()
            logger.info("Initialized event loop")
        return self._loop