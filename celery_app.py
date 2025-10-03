from celery import Celery


app = Celery(
'celery_app',
    broker='pyamqp://guest@localhost//',
    backend="redis://localhost:6379/0"
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

app.conf.update(
    include=["celery_queue.tasks"]
)

# app.autodiscover_tasks(["aire.celery_queue"])

# celery -A celery_app.app worker --loglevel=INFO