from django.urls import path

from chat.consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    path("chat/<int:chat_id>", ChatConsumer.as_asgi()),
]
