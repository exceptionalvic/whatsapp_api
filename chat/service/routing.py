"""
routing.py

This module defines WebSocket URL patterns for chat-related operations.
"""

from django.urls import re_path
from .consumers import ChatConsumer

urlpatterns = [
    # Define WebSocket URL pattern for chatroom
    re_path(r"ws/chat/(?P<chatroom_id>\w+)/$", ChatConsumer.as_asgi()),
]
