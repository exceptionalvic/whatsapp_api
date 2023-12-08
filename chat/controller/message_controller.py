"""
message_controller.py

This module defines API views for message-related operations, 
including listing messages in a chatroom and 
sending messages to a chatroom.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.entity.chat_models import Attachment, ChatRoom, Message
from chat.service.publisher import publish
from .serializers import CreateMessageSerializer, MessageSerializer
from chat.entity.chat_models import attachment_location
from chat.service.message_service import send_message, list_messages
from chat.repository.message import save_attachment
import logging
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    inline_serializer,
    OpenApiParameter,
)

@extend_schema_view(
    get=extend_schema(
        summary="List messages in a chatroom",
        description="This endpoint lists messages in a chatroom.",
        methods=["get"],
        operation_id="listChatMessages",
        tags=["Chat"],
        responses=MessageSerializer
    )
)
class MessageListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, chatroom_id: int) -> Response:
        """
        List messages in a chatroom.

        Args:
            request: The HTTP request object.
            chatroom_id: The ID of the chatroom.

        Returns:
            Response containing details of the chatroom messages.
        """
        try:
            messages = list_messages(chatroom=chatroom_id)
            serializer = self.serializer_class(messages, many=True)
            return Response({"detail": serializer.data})
        except ChatRoom.DoesNotExist:
            return Response(
                {"error": "Chatroom not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return Response(
                {"detail": "Error occurred fetching messages. Try again."},
                status=status.HTTP_404_NOT_FOUND,
            )

@extend_schema_view(
    post=extend_schema(
        summary="Send chat message in a chatroom",
        description="This endpoint sends a chat message to a chatroom.",
        methods=["post"],
        operation_id="sendChatMessages",
        tags=["Chat"],
        responses=MessageSerializer
    )
)
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateMessageSerializer

    def post(self, request, chatroom_id: int) -> Response:
        """
        Send a chat message to a chatroom.

        Args:
            request: The HTTP request object.
            chatroom_id: The ID of the chatroom.

        Returns:
            Response containing details of the sent chat message.
        """
        user = request.user
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
            content = request.data.get("content", "")
            attachment = request.data.get("attachment", None)

            message = send_message(
                content=content, sender=user, chatroom=chatroom
            )
            new_attachment = None
            if message is not None:
                if attachment is not None:
                    new_attachment = save_attachment(attachment, message)

            data = {
                "purpose": "new_chat_message",
                "chat_id": chatroom.id,
                "message": message.content,
                "file": new_attachment.file.url
                if new_attachment is not None
                else "",
                "sender": user.username,
            }

            async_to_sync(publish)(data=data)

            serializer = MessageSerializer(message)
            return Response(
                {"detail": serializer.data}, status=status.HTTP_201_CREATED
            )
        except ChatRoom.DoesNotExist:
            return Response(
                {"error": "Chatroom not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            return Response(
                {"detail": "Error sending message."},
                status=status.HTTP_400_BAD_REQUEST,
            )