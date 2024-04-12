import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.group = "private_group_" + str(self.chat_id)
        self.user = self.scope["user"]
        print("Current_user: " + str(self.user))
        # TODO need to check user can join group
        # get chat_member by current_user and chat_id
        # if chat_member found then continue connection to chat
        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )

        await self.accept()

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
