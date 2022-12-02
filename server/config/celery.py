from __future__ import absolute_import

import os

from celery import Celery, schedules

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("event_maker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check_event_time": {
        "task": "apps.events.tasks.check_event_time",
        "schedule": schedules.crontab(minute="*/5"),
    },
}
