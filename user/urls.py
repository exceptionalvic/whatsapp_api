# chat/urls.py
from django.urls import path

from user.views import UserLoginView, UserRegisterView

urlpatterns = [
    path('auth/register/', UserRegisterView.as_view(), name='user_register'),
    path('auth/login/', UserLoginView.as_view(), name='user_login'),
]
