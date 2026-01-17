from celery import Celery
import os

app = Celery(
'celery_app',
    broker = os.getenv("AMQP_URL"),
    backend = os.getenv("REDIS_URL"),
    include=["tasks"]
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

app.conf.update(
    include=["celery_config.tasks"]
)

# celery -A celery_app.app worker --loglevel=INFO