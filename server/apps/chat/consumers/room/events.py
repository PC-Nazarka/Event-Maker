class EventEventsMixin:

    async def event_users_retrieve(self, event: dict) -> None:
        await self.send_event_response(event)

    async def event_messages_retrieve(self, event: dict) -> None:
        await self.send_event_response(event)

    async def message_new(self, event: dict) -> None:
        await self.send_event_response(event)

    async def message_edit(self, event: dict) -> None:
        await self.send_event_response(event)

    async def message_remove(self, event: dict) -> None:
        await self.send_event_response(event)
