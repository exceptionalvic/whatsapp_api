"""
serializers.py

This module contains Django sample serializers for user-related 
documentation responses functionalities.
"""

import os
import jwt
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from rest_framework_simplejwt.serializers import (
    PasswordField,
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.db.models import Q
from phonenumber_field.serializerfields import PhoneNumberField

# Get the user model defined in the Django project
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Fields:
        - id
        - email
        - phone_number
        - first_name
        - last_name
        - created_at
        - updated_at
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
        ]

class SampleCredentialsSerializer(serializers.Serializer):
    """
    Serializer for the expected sample credentials response body.

    Fields:
        - access
        - refresh
    """

    access = serializers.CharField(max_length=155)
    refresh = serializers.CharField(max_length=155)

class SampleUserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for the expected user login sample response body.

    Fields:
        - id
        - email
        - phone_number
        - first_name
        - last_name
        - created_at
        - updated_at
        - credentials (SampleCredentialsSerializer)
    """

    credentials = SampleCredentialsSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "credentials",
        ]
