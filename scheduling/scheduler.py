import logging

logger = logging.getLogger(__name__)

from celery_app import app

app.conf.beat_schedule = {
    'scrape_every_min': {
        'task': 'celery_config.tasks.schedule',
        'schedule': 10,  # every 10 seconds
    },
}