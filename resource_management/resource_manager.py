import redis
import socket
import time
import logging
logger = logging.getLogger(__name__)

class ResourceManager:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def can_run(self, request) -> bool:
        airline = request.airline
        worker_ip = socket.gethostbyname(socket.gethostname())
        key = f"last_scrape:{airline}:{worker_ip}"
        last = self.r.get(key)
        now = time.time()

        if last and now - float(last) < 10:
            logger.info(f"Cannot scrape {airline} from {worker_ip} (rate limit)")
            return False

        logger.info(f"Can scrape {airline} from {worker_ip}")
        self.r.set(key, str(now))
        return True
