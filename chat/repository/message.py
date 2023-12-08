"""
repositories.py

This module provides repository methods for 
sql interactions with Message and Attachment models.
"""

from chat.entity.chat_models import Attachment, Message, ChatRoom

class MessageRepository:
    @staticmethod
    def create_message(content, sender, chatroom):
        """
        Create a new message in the specified chatroom.

        Args:
            content: The content of the message.
            sender: The user sending the message.
            chatroom: The chatroom to which the message belongs.

        Returns:
            Message: The created message.
        """
        message = Message(content=content, sender=sender, chatroom=chatroom)
        message.save()
        return message

    @staticmethod
    def get_messages(chatroom):
        """
        Retrieve all messages in the specified chatroom.

        Args:
            chatroom: The chatroom from which to retrieve messages.

        Returns:
            QuerySet: QuerySet of messages in the chatroom, 
            ordered by creation time.
        """
        messages = Message.objects.filter(chatroom=chatroom).order_by(
            "created_at"
        )
        return list(messages)

def save_attachment(attachment, message_id):
    """
    Save an attachment for a given message.

    Args:
        attachment: The file attachment.
        message_id: The ID of the message to which the attachment belongs.

    Returns:
        Attachment: The created attachment.
    """
    new_attachment = Attachment.objects.create(
        message=message_id, file=attachment
    )

    # TODO: Upload file in chunks for scalability. 
    # Untested sample code implementation below:
    # with open(attachment.url, 'wb+') as destination:
    #     for chunk in attachment.chunks():
    #         destination.write(chunk)
    return new_attachment
