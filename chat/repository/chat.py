"""
repositories.py

This module provides repository methods for 
sql interactions with ChatRoom models.
"""

from chat.models import ChatRoom


class ChatRoomRepository:
    @staticmethod
    def perform_create_chatroom(user, name, members):
        """
        Create a new chatroom with the specified user 
        as the admin and given members.

        Args:
            user: The user creating the chatroom.
            name: The name of the chatroom.
            members: List of users to be added to the chatroom.

        Returns:
            ChatRoom: The created chatroom.
        """
        if members is None:
            members = [user]
        else:
            members.append(user)
        chatroom = ChatRoom(name=name, admin=user)
        chatroom.save()

        if members:
            chatroom.members.set(members)
        return chatroom

    @staticmethod
    def fetch_chatrooms(user):
        """
        Fetch all chatrooms that the user is a member of.

        Args:
            user: The user whose chatrooms are to be fetched.

        Returns:
            QuerySet: QuerySet of chatrooms that the user is a member of.
        """
        try:
            return ChatRoom.objects.filter(members=user)
        except ChatRoom.DoesNotExist:
            return None

    @staticmethod
    def exit_chatroom(user, chatroom):
        """
        Remove the user from the specified chatroom.

        Args:
            user: The user leaving the chatroom.
            chatroom: The chatroom to leave.

        Returns:
            ChatRoom or None: The chatroom after the user has left,
            or None if the user is not a member.
        """
        get_chatroom = ChatRoom.objects.filter(id=chatroom).first()
        if get_chatroom is not None and user in get_chatroom.members.all():
            get_chatroom.members.remove(user)
            return get_chatroom
        elif not get_chatroom is not None:
            return None
        else:
            return None

    @staticmethod
    def join_chatroom(user, chatroom):
        """
        Add the user to the specified chatroom.

        Args:
            user: The user joining the chatroom.
            chatroom: The chatroom to join.

        Returns:
            ChatRoom or str: The chatroom after the user has joined,
            or "chatroom filled" if the chatroom is full.
        """
        if ChatRoom.objects.filter(id=chatroom).count() >= 1024:
            return "chatroom filled"
        get_chatroom = ChatRoom.objects.filter(id=chatroom).first()
        if get_chatroom is not None and user in get_chatroom.members.all():
            return None
        elif not get_chatroom is not None:
            return None
        get_chatroom.members.add(user)
        return get_chatroom
