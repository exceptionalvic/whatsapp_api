"""
chatroom_controller.py

This module defines API views for chatroom-related operations, 
including creating a chatroom,leaving a chatroom, joining a chatroom, 
and listing a user's chatrooms.
"""

# Import necessary modules
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
import logging
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    inline_serializer,
    OpenApiParameter,
)

from chat.entity.chat_models import ChatRoom
from chat.controller.serializers import (
    ChatRoomSerializer,
    CreateChatRoomSerializer,
)

from chat.service.publisher import publish
from chat.service.chatroom_service import (
    create_chatroom,
    list_chatrooms,
    leave_chatroom,
    enter_chatroom,
)

from chat.service.publisher import publish


@extend_schema_view(
    post=extend_schema(
        summary="Create a chatroom",
        description="This endpoint creates a chatroom",
        methods=["post"],
        operation_id="userChatRoomCreate",
        tags=["Chat"],
        responses=ChatRoomSerializer,
    )
)
class ChatRoomCreateView(APIView):
    # Set permission classes and serializer class for the view
    permission_classes = [IsAuthenticated]
    serializer_class = CreateChatRoomSerializer

    def post(self, request):
        """
        Create a new chatroom.

        Args:
            request: The HTTP request object.

        Returns:
            Response containing details of the created chatroom or errors.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            members = serializer.validated_data.get("members", [])
            name = serializer.validated_data.get("name")

            chatroom = create_chatroom(request, name, members)

            chatroom_data = ChatRoomSerializer(chatroom).data
            return Response(
                {"chatroom": chatroom_data}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        summary="Exit a chatroom",
        description="This endpoint exits a chatroom",
        methods=["post"],
        operation_id="userChatRoomExit",
        tags=["Chat"],
        responses=inline_serializer(
            name="Empty serializer for example.",
            fields={"detail": serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                "Example of response body.",
                value={"detail": "JohnDoe has left the Chatroom"},
                request_only=False,
                response_only=True,
            ),
        ],
    )
)
class ChatRoomLeaveView(APIView):
    # Set permission classes for the view
    permission_classes = [IsAuthenticated]

    def post(self, request, chatroom_id) -> JsonResponse:
        """
        Exit a chatroom.

        Args:
            request: The HTTP request object.
            chatroom_id: The ID of the chatroom to exit.

        Returns:
            Response indicating success or failure.
        """
        user = request.user
        try:
            chatroom = leave_chatroom(user=user, chatroom=chatroom_id)
            if chatroom is not None:
                data = {
                    "purpose": "new_chat_message",
                    "chat_id": chatroom_id,
                    "message": f"{user.username} has left the chatroom",
                    "sender": "WhatsApp MessengerBot",
                }

                # Publish this data to rabbitmq queue so it can
                # be fetched and sent to the websocket room.
                async_to_sync(publish)(data=data)
                return Response(
                    {"detail": f"{user.username} have left the chatroom"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": f"User not in chatroom"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except ChatRoom.DoesNotExist:
            return Response(
                {"detail": "Chatroom not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


@extend_schema_view(
    post=extend_schema(
        summary="Join a chat room",
        description="This endpoint is for chatroom",
        methods=["post"],
        operation_id="joinChatRoom",
        tags=["Chat"],
        responses=inline_serializer(
            name="Empty serializer for example.",
            fields={"detail": serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                "Example of response body.",
                value={
                    "detail": "You have successfully joined the chatroom"
                },
                request_only=False,
                response_only=True,
            ),
        ],
    )
)
class ChatRoomEnterView(APIView):
    # Set permission classes for the view
    permission_classes = [IsAuthenticated]

    def post(self, request, chatroom_id):
        """
        Join a chatroom.

        Args:
            request: The HTTP request object.
            chatroom_id: The ID of the chatroom to join.

        Returns:
            Response indicating success or failure.
        """
        user = request.user
        try:
            # join current chatroom
            chatroom = enter_chatroom(user=user, chatroom=chatroom_id)
            if chatroom is not None:
                data = {
                    "purpose": "new_chat_message",
                    "chat_id": chatroom.id,
                    "message": f"{user.username} just joined the Chatroom",
                    "sender": "WhatsApp MessengerBot",
                }

                # Publish this data to rabbitmq queue so it can
                # be fetched and sent to the websocket room.
                async_to_sync(publish)(data=data)
                return Response(
                    {
                        "detail": f"You have successfully joined the chatroom: {chatroom.name}"
                    },
                    status=status.HTTP_200_OK,
                )
            elif chatroom == "chatroom filled":
                return Response(
                    {"detail": "Maximum chatroom members exceeded."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                return Response(
                    {"detail": "Chatroom already joined by you"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ChatRoom.DoesNotExist:
            return Response(
                {"detail": "Chatroom not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logging.error(f"Error entering chatroom: {str(e)}")
            return Response(
                {"detail": "Chatroom join not successful"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema_view(
    get=extend_schema(
        summary="List User's Chat Rooms",
        description="List User's Chat Rooms",
        methods=["get"],
        operation_id="userChatRoomList",
        tags=["Chat"],
        responses=ChatRoomSerializer,
    )
)
class ChatRoomListView(APIView):
    # Set permission classes and serializer class for the view
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get(self, request):
        """
        List all chatrooms for a user.

        Args:
            request: The HTTP request object.

        Returns:
            Response containing details of the user's chatrooms.
        """
        user = request.user
        try:
            # perform sql query to list chatrooms current user is a member of.
            chatrooms = list_chatrooms(user=user)

            serializer = self.serializer_class(chatrooms, many=True)
            return Response(
                {"chatrooms": serializer.data}, status=status.HTTP_200_OK
            )
        except ChatRoom.DoesNotExist:
            return Response(
                {"detail": "Chatroom not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
