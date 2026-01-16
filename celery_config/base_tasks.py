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
    _proxy_mgr: ProxyManager = None

    @property
    def proxy_mgr(self):
        if self._proxy_mgr is None:
            self._proxy_mgr = ProxyManager([])
            logger.info("Initialized proxy manager")
        return self._proxy_mgr