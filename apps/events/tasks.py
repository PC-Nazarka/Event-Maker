from datetime import datetime, timezone

from apps.core.services import send_email
from config.celery_app import app

from . import models


@app.task
def check_event_time() -> None:
    """Check time of events and send email this remember."""
    for event in models.Event.objects.filter(is_finished=False):
        minutes = (event.datetime_spending - datetime.now(timezone.utc)) // 60
        if minutes in range(0, 6):
            send_email("soon", event)
