# import json
# import pytest
# from user.models import User
# from django.test import Client
# from rest_framework import status
# from chat.entity.chat_models import ChatRoom, Message
# from chat.controller.serializers import MessageSerializer, CreateMessageSerializer

# # Assuming that your Django app is named 'chat'
# from chat.service.message_service import list_messages, send_message
# from chat.repository.message import save_attachment

# @pytest.fixture
# def client():
#     return Client()

# @pytest.fixture
# def create_user():
#     return User.objects.create_user(email='test@test.com', username='testuser', password='testpassword')

# @pytest.fixture
# def create_chatroom(create_user):
#     # Create a user
#     user = create_user()

#     # Create a ChatRoom instance
#     chatroom = ChatRoom.objects.create(name='Test Chatroom')

#     # Add the user as a member of the chatroom
#     chatroom.members.add(user)

#     return chatroom

# @pytest.mark.django_db
# def test_message_list_view(client, create_user, create_chatroom):
#     url = f'/api/v1/chat/chatrooms/{create_chatroom.id}/messages/'

#     client.force_login(create_user)
#     response = client.get(url)

#     assert response.status_code == status.HTTP_200_OK
#     assert 'detail' in response.data

# @pytest.mark.django_db
# def test_send_message_view(client, create_user, create_chatroom):
#     url = f'/api/v1/chat/chatrooms/{create_chatroom.id}/messages/send/'

#     client.force_login(create_user)
    
#     content = 'Test message'
#     attachment_data = {'file': 'sample_test_file.jpg', 'content_type': 'image/jpeg'}
#     # data = {'content': content}
#     data = {'content': content, 'attachment': attachment_data}

#     response = client.post(url, data=json.dumps(data), content_type='application/json')

#     assert response.status_code == status.HTTP_201_CREATED
#     assert 'detail' in response.data

#     # Additional assertions if needed, e.g., checking the message content in the database
#     messages = list_messages(chatroom=create_chatroom.id)
#     assert messages.count() == 1
#     assert messages[0].content == content

#     # If testing attachment handling, you can add assertions for attachments
#     assert 'file' in response.data
#     assert response.data['file'] == save_attachment(attachment_data, messages[0]).file.url


import pytest
from rest_framework.test import APIClient
from user.models import User
from chat.entity.chat_models import ChatRoom, Message
from chat.service.message_service import list_messages

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(email='test@test.com',username='testuser', password='testpassword')

@pytest.fixture
def chatroom(user):
    room = ChatRoom.objects.create(name='Test Chatroom')
    room.members.add(user)
    return room

@pytest.fixture
def message(user, chatroom):
    return Message.objects.create(content='Test message', sender=user, chatroom=chatroom)

@pytest.mark.django_db
def test_message_list_view(api_client, user, chatroom, message):
    api_client.force_authenticate(user=user)
    url = f'/api/v1/chat/chatrooms/{chatroom.id}/messages/'

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['detail'][0]['content'] == message.content


@pytest.mark.django_db
def test_send_message_view(api_client, user, chatroom):
    api_client.force_authenticate(user=user)
    url = f'/api/v1/chat/chatrooms/{chatroom.id}/messages/send/'

    data = {'content': 'Test message'}

    response = api_client.post(url, data)

    assert response.status_code == 201
    assert 'detail' in response.data


@pytest.mark.django_db
def test_send_message_view_with_attachment(api_client, user, chatroom):
    api_client.force_authenticate(user=user)
    url = f'/api/v1/chat/chatrooms/{chatroom.id}/messages/send/'

    data = {'content': 'Test message', 'attachment': 'attachment_content'}

    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert 'detail' in response.data
    assert 'attachment' in response.data['detail']


@pytest.mark.django_db
def test_send_message_view_chatroom_not_found(api_client, user):
    api_client.force_authenticate(user=user)
    url = '/api/v1/chat/chatrooms/999/messages/send/'

    data = {'content': 'Test message'}

    response = api_client.post(url, data)

    assert response.status_code == 404
    assert 'error' in response.data

