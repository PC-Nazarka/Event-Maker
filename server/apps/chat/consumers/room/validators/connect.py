from typing import Optional

from django.contrib.auth.models import User

from ..queries import EventQueries


class ConnectValidation:

    @staticmethod
    async def validate(user: User, event_id: int) -> Optional[str]:
        if isinstance(event_id, str) and not event_id.isdigit():
            return "Enter right primary key of event"
        event_id = int(event_id)
        if not (await EventQueries.check_event_exists(event_id)):
            return "Event doesn't exists"
        consist_user = await EventQueries.check_user_consist_in_event(
            user.id,
            event_id,
        )
        if not consist_user:
            return "User isn't member of event"
