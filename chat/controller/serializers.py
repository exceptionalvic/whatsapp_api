"""
serializers.py

This module defines serializers for ChatRoom and 
Message models in the chat application.
"""

from rest_framework import serializers
from chat.entity.chat_models import Attachment, ChatRoom, Message
from asgiref.sync import async_to_sync

class ChatRoomSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatRoom model.

    Attributes:
        members (SerializerMethodField): Serializer method field 
        to retrieve members of the chat room.

    Meta:
        model: The ChatRoom model.
        fields: All fields from the ChatRoom model.

    Methods:
        get_members: Method to retrieve members of the chat room.
    """
    members = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = "__all__"

    def get_members(self, obj):
        data = []
        if obj.members:
            for member in obj.members.all():
                data.append({"id": member.id, "username": member.username})
        return data

class CreateChatRoomSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new chat room.

    Attributes:
        members (ListField): List of members for the chat room.

    Meta:
        model: The ChatRoom model.
        fields: "name" and "members".

    """
    members = serializers.ListField(required=False)

    class Meta:
        model = ChatRoom
        fields = ["name", "members"]

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.

    Attributes:
        attachment (SerializerMethodField): Serializer 
        method field to retrieve attachment URL.

    Meta:
        model: The Message model.
        fields: All fields from the Message model and "attachment".

    Methods:
        get_attachment: Method to retrieve attachment URL for a message.
    """
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", "content", "sender", "chatroom", "attachment", "created_at"]

    def get_attachment(self, obj):
        attachment = Attachment.objects.filter(message=obj).first()
        if attachment is not None:
            attachment_url = attachment.file.url
            return attachment_url
        return None

class CreateMessageSerializer(serializers.Serializer):
    """
    Serializer for creating a new message.

    Attributes:
        content (CharField): The content of the message.
        attachment (FileField): The file attachment for the message.
    """
    content = serializers.CharField(required=True)
    attachment = serializers.FileField(required=False)

class FetchMessageListSerializer(serializers.ModelSerializer):
    """
    Serializer for fetching a list of messages.

    Meta:
        model: The Message model.
        fields: "chatroom".
    """
    class Meta:
        model = Message
        fields = ["chatroom"]
