# import redis
# import time
# from typing import Optional
#
#
# class RateManager:
#     def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
#         # Redis connection
#         self.r = redis.Redis(host=host, port=port, db=db)
#
#     def acquire(self, site: str, cooldown: int) -> bool:
#         """
#         Try to acquire permission to scrape a site.
#         Returns True if successful, False if rate-limited.
#
#         :param site: Airline identifier (Ex. AC)
#         :param cooldown: Minimum seconds between scrapes for this site
#         """
#         key = f"rate_limit:{site}"
#         now = int(time.time())
#
#         # SET with NX + EX = only sets if not exists, auto expires
#         acquired = self.r.set(name=key, value=now, nx=True, ex=cooldown)
#
#         return acquired
#
#     def time_left(self, site: str) -> Optional[int]:
#         """
#         Returns TTL (time to wait) for the site's lock, or None if free.
#         """
#         key = f"rate_limit:{site}"
#         ttl = self.r.ttl(key)
#         if ttl == -2:  # Key does not exist
#             return None
#         return ttl
#
#     def force_release(self, site: str):
#         """
#         Manually release a site.
#         """
#         key = f"rate_limit:{site}"
#         self.r.delete(key)
