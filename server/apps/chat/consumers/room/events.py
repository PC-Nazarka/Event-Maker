class EventEventsMixin:

    async def event_users_retrieve(self, event: dict) -> None:
        await self.send_event_response(event)

    async def event_messages_retrieve(self, event: dict) -> None:
        await self.send_event_response(event)
