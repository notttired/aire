import asyncio, logging
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)
from celery_queue.tasks import schedule

from celery.schedules import crontab
from celery_app import app

app.conf.beat_schedule = {
    'scrape_every_min': {
        'task': 'celery_queue.tasks.schedule',
        'schedule': 10,  # every 10 seconds
    },
}