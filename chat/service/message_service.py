"""
message_service.py

This module provides services related to handling messages in a chatroom.
"""

# Import necessary modules
from chat.entity.chat_models import Attachment, Message, ChatRoom
from chat.repository.message import MessageRepository

def send_message(content, sender, chatroom):
    """
    Send a message to a chatroom.

    Args:
        content (str): The content of the message.
        sender: The user sending the message.
        chatroom: The chatroom to which the message is sent.

    Returns:
        The created message object.
    """
    return MessageRepository.create_message(content, sender, chatroom)

def list_messages(chatroom):
    """
    List all messages in a given chatroom.

    Args:
        chatroom: The chatroom for which to fetch messages.

    Returns:
        List of message objects.
    """
    return MessageRepository.get_messages(chatroom)
