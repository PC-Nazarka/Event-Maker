from typing import Final


class Actions:
    USER_LIST: Final[str] = "user_list"
    MESSAGES_LIST: Final[str] = "messages_list"
    SEND_MESSAGES: Final[str] = "send_message"
    EDIT_MESSAGE: Final[str] = "edit_message"
    REMOVE_MESSAGE: Final[str] = "remove_message"


class Events:
    EVENT_USERS_RETRIEVE: Final[str] = "event_users_retrieve"
    EVENT_MESSAGES_RETRIEVE: Final[str] = "event_messages_retrieve"
    MESSAGE_NEW: Final[str] = "message_new"
    MESSAGE_EDIT: Final[str] = "message_edit"
    MESSAGE_REMOVE: Final[str] = "message_remove"
