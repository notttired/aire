from typing import Dict, List
import asyncio

# Type alias for Playwright proxy configs
ProxyDict = Dict[str, str]

class ProxyManager:
    def __init__(self, proxies: List[ProxyDict]):
        self._queue: asyncio.Queue[ProxyDict] = asyncio.Queue()
        for proxy in proxies:
            self._queue.put_nowait(proxy)

    async def acquire(self) -> ProxyDict:
        """
        Get the next available proxy.
        Blocks if no proxies are currently free.
        """
        proxy = await self._queue.get()
        return proxy

    async def release(self, proxy: ProxyDict):
        """
        Return a proxy back into the pool.
        """
        await self._queue.put(proxy)

    def size(self) -> int:
        """Number of proxies currently available in the pool."""
        return self._queue.qsize()