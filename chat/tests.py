# import json
# import pytest
# from django.contrib.auth.models import User
# from django.test import Client
# from rest_framework import status
# from chat.entity.chat_models import ChatRoom

# # Assuming that your Django app is named 'chat'
# from chat.controller.serializers import ChatRoomSerializer, CreateChatRoomSerializer

# @pytest.fixture
# def client():
#     return Client()

# @pytest.fixture
# def create_user():
#     return User.objects.create_user(username='testuser', password='testpassword')

# @pytest.fixture
# def create_chatroom():
#     return ChatRoom.objects.create(name='Test Chatroom')

# def test_chatroom_create_view(client, create_user):
#     url = '/api/v1/chat/chatrooms/create/'
#     data = {
#         'name': 'Test Chatroom',
#         'members': [create_user.id],
#     }

#     client.force_login(create_user)
#     response = client.post(url, data=json.dumps(data), content_type='application/json')

#     assert response.status_code == status.HTTP_201_CREATED
#     assert 'chatroom' in response.data

# def test_chatroom_leave_view(client, create_user, create_chatroom):
#     url = f'/api/v1/chat/chatrooms/{create_chatroom.id}/leave/'

#     client.force_login(create_user)
#     response = client.post(url)

#     assert response.status_code == status.HTTP_200_OK
#     assert 'detail' in response.data

# def test_chatroom_enter_view(client, create_user, create_chatroom):
#     url = f'/api/v1/chat/chatrooms/{create_chatroom.id}/enter/'

#     client.force_login(create_user)
#     response = client.post(url)

#     assert response.status_code == status.HTTP_200_OK
#     assert 'detail' in response.data

# def test_chatroom_list_view(client, create_user, create_chatroom):
#     url = '/api/v1/chat/chatrooms/'

#     client.force_login(create_user)
#     response = client.get(url)

#     assert response.status_code == status.HTTP_200_OK
#     assert 'chatrooms' in response.data
