"""
chat_models.py

This module defines Django models for chat-related entities, including ChatRoom, Message, and Attachment.
"""

from django.db import models
from user.models import User
from chat.mixins import TimeStampMixin

def attachment_location(instance, filename):
    """
    Determine the upload location for attachments based on the file type.

    Args:
        instance: The Attachment instance.
        filename: The original filename of the attachment.

    Returns:
        str: The upload location for the attachment.
    Raises:
        ValueError: If the file type is not supported.
    """
    file_extension = filename.split(".")[-1].lower()
    is_file_an_image = file_extension in [
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "svg",
        "webp",
        "ico",
    ]
    is_file_a_video = file_extension in [
        "mp4",
        "avi",
        "mkv",
        "mov",
        "wmv",
        "flv",
        "webm",
        "3gp",
    ]

    if is_file_an_image:
        return f"root/image/{filename}"
    elif is_file_a_video:
        return f"root/video/{filename}"
    else:
        # Raise an exception if file type is not supported
        raise ValueError(f"Unsupported file type: {file_extension}")

class ChatRoom(TimeStampMixin, models.Model):
    """
    Model representing a chat room.

    Attributes:
        name (str): The name of the chat room.
        members (ManyToManyField): Users who are members of the chat room.
        admin (ForeignKey): The admin of the chat room.
        created_at (DateTimeField): The timestamp of when the chat room was created.

    Meta:
        ordering: The default ordering for chat rooms based on creation time.

    Methods:
        __str__: Returns a string representation of the chat room.
    """

    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    admin = models.ForeignKey(
        User,
        related_name="chatroom_admin",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.name} - Admin: {self.admin.username}; Created: {self.created_at}"


class Message(TimeStampMixin, models.Model):
    """
    Model representing a message in a chat room.

    Attributes:
        sender (ForeignKey): The user who sent the message.
        chatroom (ForeignKey): The chat room to which the message belongs.
        content (TextField): The content of the message.
        created_at (DateTimeField): The timestamp of when the message was created.
    """

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()

class Attachment(TimeStampMixin, models.Model):
    """
    Model representing an attachment in a chat message.

    Attributes:
        message (ForeignKey): The message to which the attachment belongs.
        file (FileField): The file attachment.
        created_at (DateTimeField): The timestamp of when the attachment was created.
    """

    message = models.ForeignKey(
        Message,
        related_name="message_attachment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    file = models.FileField(
        upload_to=attachment_location, max_length=455, null=True, blank=True
    )
