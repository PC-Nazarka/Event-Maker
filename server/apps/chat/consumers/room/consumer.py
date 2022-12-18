from channels.exceptions import DenyConnection

from apps.core.consumer import BaseConsumer

from .actions import EventActionsMixin
from .constants import Actions
from .events import EventEventsMixin
from .validators import ConnectValidation


class ChatConsumer(
    BaseConsumer,
    EventActionsMixin,
    EventEventsMixin,
):

    ACTION_MAP = {
        Actions.USER_LIST: EventActionsMixin.user_list,
        Actions.MESSAGES_LIST: EventActionsMixin.message_list,
    }

    async def connect(self):
        self.event_id = self.scope["url_route"]["kwargs"]["event_id"]
        self.group_name = f"room_event_{self.event_id}"
        self.user = self.scope["user"]
        await self.accept()
        if error := await ConnectValidation.validate(
            self.user,
            self.event_id,
        ):
            await self.send_error(error)
            raise DenyConnection()
        self.event_id = int(self.event_id)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await EventActionsMixin.user_list(self)
        await EventActionsMixin.message_list(self)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )
        await self.close()
