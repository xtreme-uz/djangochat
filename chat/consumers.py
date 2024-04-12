import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import ChatMember


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.group = "private_group_" + str(self.chat_id)
        self.user_id = self.scope["user"].id
        self.chat_member_exists = await self.validate_user()
        if self.chat_member_exists:
            await self.channel_layer.group_add(
                self.group,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = {
            "type": "sendMessage",
            "message": text_data_json["message"],
            "username": text_data_json["username"],
        }
        await self.channel_layer.group_send(self.group, message)

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))

    @database_sync_to_async
    def validate_user(self):
        return ChatMember.objects.filter(chat_id=self.chat_id, member_id=self.user_id).exists()
