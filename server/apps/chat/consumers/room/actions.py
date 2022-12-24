from .constants import Events
from .queries import EventQueries, MessageQueries
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

    async def send_message(self, body: dict) -> None:
        data = {
            "message": body["message"],
            "event": await EventQueries.get_event_by_id(self.event_id),
            "user": self.user,
        }
        message = await MessageQueries.create_message(data)
        body = {"message": await EventService.get_message(message)}
        await self.response_to_group(Events.MESSAGE_NEW, body)

    async def edit_message(self, body: dict) -> None:
        id = body.pop("id")
        if (await MessageQueries.check_message_owner(
            id,
            self.user.id,
        )):
            await MessageQueries.update_message(
                id,
                body,
            )
            message = await MessageQueries.get_message_by_id(id)
            body = {"message": await EventService.get_message(message)}
            await self.response_to_group(Events.MESSAGE_EDIT, body)

    async def remove_message(self, body: dict) -> None:
        id = body.pop("id")
        if (await MessageQueries.check_message_owner(
            id,
            self.user.id,
        )):
            await MessageQueries.delete_message(id)
            body = {"message_id": id}
            await self.response_to_group(Events.MESSAGE_REMOVE, body)
