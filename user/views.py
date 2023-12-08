"""
Views for user app
"""

import logging
import jwt
from django.conf import settings
from smtplib import SMTPException
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
import json
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from user.serializers import UserLoginSerializer, UserRegisterSerializer, UserSerializer
from user.documentation_serializers import SampleUserLoginSerializer
from chat.utils.renderers import LoginRenderer, UserResponseRenderer
from rest_framework.authtoken.models import Token
from requests.exceptions import HTTPError
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Get the user model defined in the Django project
User = get_user_model()

@extend_schema_view(
    post=extend_schema(
        summary="User Sign In",
        description="User sign in.",
        methods=["post"],
        operation_id="userLogin",
        tags=["User"],
        responses=SampleUserLoginSerializer,
    )
)
class UserLoginView(TokenObtainPairView):
    """
    View for user login using JWT authentication.
    """

    serializer_class = UserLoginSerializer
    renderer_classes = [LoginRenderer]
    permission_classes = [AllowAny]
    authentication_classes = []

@extend_schema_view(
    post=extend_schema(
        summary="Register User",
        description="Register user.",
        methods=["post"],
        operation_id="userRegister",
        tags=["User"],
        responses=SampleUserLoginSerializer,
    )
)
class UserRegisterView(APIView):
    """
    View for user registration.
    """

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user registration.

        Returns:
            Response: Serialized user and authentication credentials.
        """
        # Initialize serializer class
        ser = self.serializer_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            # Check if account with email exists
            user_email_exists = User.objects.filter(
                email=request.data["email"]
            ).exists()

            if user_email_exists:
                return Response(
                    {"detail": "User account already exists. Please login."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Save user and set password
            user = ser.save()
            password = request.data["password"]
            user.set_password(password)
            user.save()

            # Generate authentication credentials
            refresh = RefreshToken.for_user(user)
            data = {
                "user": UserSerializer(user).data,
                "credentials": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
        )
