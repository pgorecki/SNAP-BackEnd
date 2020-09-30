import os
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

import configurations
from configurations.importer import installed

if not installed:
    configurations.setup()

from celery import Celery
from celery.result import AsyncResult
from celery.schedules import crontab


app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    "update_eligibity_queue": {
        "task": "eligibility.tasks.enqueue_eligibility",
        "schedule": crontab(minute=0, hour=0, day_of_month="1"),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print("Task {0} raised exception: {1!r}\n{2!r}".format(uuid, exc, result.traceback))
