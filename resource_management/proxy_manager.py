from typing import Dict, List
import asyncio

# Type alias for Playwright proxy configs
ProxyDict = Dict[str, str]

class ProxyManager:
    def __init__(self, proxies: List[ProxyDict]):
        self._queue: asyncio.Queue[ProxyDict] = asyncio.Queue()
        for proxy in proxies:
            self._queue.put_nowait(proxy)

    async def acquire(self) -> ProxyDict | None:
        """
        Get the next available proxy.
        Blocks if no proxies are currently free.
        """
        if self._queue.empty():
            return None
        proxy = await self._queue.get()
        return proxy

    async def release(self, proxy: ProxyDict | None) -> None:
        if not proxy:
            return None
        """
        Return a proxy back into the pool.
        """
        await self._queue.put(proxy)
        return None