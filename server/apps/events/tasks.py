from datetime import datetime, timezone

from apps.core.services import send_email
from config.celery import app

from . import models


@app.task
def check_event_time() -> None:
    """Check time of events and send email this remember."""
    events = models.Event.objects.prefetch_related(
        "members"
    ).filter(is_finished=False).values(
        "name",
        "datetime_spending",
        "members__email",
    )
    for event in events:
        minutes = (
            event["datetime_spending"] -
            datetime.now(timezone.utc)
        ) // 60
        if minutes in range(0, 6):
            send_email("soon", event["name"], [event["members__email"]])


@app.task
def send_email_invite(invite_id: int) -> None:
    """Send email about invite."""
    data = models.Invite.objects.select_related(
        "event", "user",
    ).filter(id=invite_id,).values("event__name", "user__email").first()
    send_email("invite", data["event__name"], [data["user__email"]])
