# chat/urls.py
from django.urls import path

from chat.controller import chatroom_controller, message_controller

urlpatterns = [
    path(
        "chatrooms/",
        chatroom_controller.ChatRoomListView.as_view(),
        name="list_chatrooms",
    ),
    path(
        "chatrooms/create/",
        chatroom_controller.ChatRoomCreateView.as_view(),
        name="create_chatroom",
    ),
    path(
        "chatrooms/<int:chatroom_id>/leave/",
        chatroom_controller.ChatRoomLeaveView.as_view(),
        name="leave_chatroom",
    ),
    path(
        "chatrooms/<int:chatroom_id>/enter/",
        chatroom_controller.ChatRoomEnterView.as_view(),
        name="enter_chatroom",
    ),
    path(
        "chatrooms/<int:chatroom_id>/messages/",
        message_controller.MessageListView.as_view(),
        name="list_messages",
    ),
    path(
        "chatrooms/<int:chatroom_id>/messages/send/",
        message_controller.SendMessageView.as_view(),
        name="send_message",
    ),
]

