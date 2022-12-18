from typing import Final


class Actions:
    USER_LIST: Final[str] = "user_list"
    MESSAGES_LIST: Final[str] = "messages_list"


class Events:
    EVENT_USERS_RETRIEVE: Final[str] = "event_users_retrieve"
    EVENT_MESSAGES_RETRIEVE: Final[str] = "event_messages_retrieve"
