# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from chat.entity.chat_models import Message, ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_id = self.scope["url_route"]["kwargs"]["chatroom_id"]
        self.chatroom_group_name = f"chat_{self.chatroom_id}"
        print("Room:", self.chatroom_group_name)
        print("User:", self.scope.get("user"))
        # Join room group
        await self.channel_layer.group_add(
            self.chatroom_group_name, self.channel_name
        )

        await self.check_chatroom_user_membership_status(
            self.chatroom_id, self.scope.get("user")
        )
        # await self.check_if_user_is_a_chatroom_member
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chatroom_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("text_data_json:", text_data_json)
        purpose = text_data_json["purpose"]

        if purpose == "send_chat_message":
            message = text_data_json["message"]
            sender = self.scope["user"]

            # Save message to the database
            await self.save_message(sender, message)

            data = {
                "purpose": "new_chat_message",
                "message": message,
                "sender": sender.username,
            }

            # Send message to room group
            await self.channel_layer.group_send(
                self.chatroom_group_name,
                {
                    "type": "chat.message",
                    "data": data,
                },
            )

    async def chat_message(self, event):
        print("EVEEEEENNNNNT:", event)
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "data": event["data"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, sender, message):
        chatroom_id = int(self.chatroom_id)
        chatroom = ChatRoom.objects.get(id=chatroom_id)
        Message.objects.create(
            content=message, sender=self.scope["user"], chatroom=chatroom
        )

    @database_sync_to_async
    def check_chatroom_user_membership_status(self, chatroom_id, user):
        get_chatroom = ChatRoom.objects.filter(id=chatroom_id).first()
        if get_chatroom is not None:
            # check if a user is a Chatroom member
            check_membership = ChatRoom.objects.filter(members=user).exists()
            if check_membership:
                pass
            else:
                # reject a user who is not a Chatroom member
                async_to_sync(self.close)()
