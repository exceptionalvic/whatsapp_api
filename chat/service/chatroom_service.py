"""
This module provide services related to chatrooms, including creating new chatrooms,
listing existing chatrooms for a user, leaving a chatroom, and joining a chatroom.
"""
from chat.repository.chat import ChatRoomRepository


def create_chatroom(request, name, members):
    """
    Create a new chatroom.

    Args:
        request: The request object containing user information.
        name (str): The name of the chatroom.
        members (list): List of members to be added to the chatroom.

    Returns:
        The created chatroom object.
    """
    user = request.user
    return ChatRoomRepository.perform_create_chatroom(user, name, members)


def list_chatrooms(user):
    """
    List all chatrooms for a given user.

    Args:
        user: The user for whom to fetch chatrooms.

    Returns:
        List of chatroom objects.
    """
    return ChatRoomRepository.fetch_chatrooms(user=user)


def leave_chatroom(user, chatroom):
    """
    Leave a chatroom.

    Args:
        user: The user who is leaving the chatroom.
        chatroom: The chatroom to leave.

    Returns:
        Response object indicating success or failure.
    """
    return ChatRoomRepository.exit_chatroom(user, chatroom)


def enter_chatroom(user, chatroom):
    """
    Enter a chatroom.

    Args:
        user: The user who is entering the chatroom.
        chatroom: The chatroom to join.

    Returns:
        Response object indicating success or failure.
    """
    return ChatRoomRepository.join_chatroom(user, chatroom)
