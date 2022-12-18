from .constants import Events
from .queries import EventQueries
from .services import EventService


class EventActionsMixin:

    async def user_list(self) -> None:
        members = await EventQueries.get_members_list(self.event_id)
        body = {"members": await EventService.get_members_list(members)}
        await self.response_to_user(Events.EVENT_USERS_RETRIEVE, body)

    async def message_list(self) -> None:
        messages = await EventQueries.get_messages_list(self.event_id)
        body = {"messages": await EventService.get_messages_list(messages)}
        await self.response_to_user(Events.EVENT_MESSAGES_RETRIEVE, body)
