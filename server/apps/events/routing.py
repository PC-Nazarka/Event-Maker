from django.urls import path

from . import consumers

chat_websocket_urlpatterns = [
    path("ws/chat/<chat_name>/", consumers.ChatConsumer.as_asgi()),
]
