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


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """user serializer"""

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


class UserLoginSerializer(TokenObtainPairSerializer):
    """Login serializer for auth user"""
    
    # declare user serializer to be included in login response
    auth_serializer = UserSerializer  

    def __init__(self, *args, **kwargs):
        """Overriding to change the error messages."""
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(
            error_messages={
                "blank": "Looks like you submitted wrong data. Please check and try again"
            }
        )
        self.fields["password"] = PasswordField(
            error_messages={
                "blank": "Looks like you submitted wrong data. Please check and try again"
            }
        )

    def validate(self, attrs):
        """Overriding to add user to responses"""
        token_data = super().validate(attrs)

        data = {}
        data["user"] = self.auth_serializer(self.user).data
        data["credentials"] = {**token_data}
        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    """Seralizer for user registration."""

    email = serializers.EmailField(max_length=255, required=True)
    phone_number = PhoneNumberField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=255,
        required=True,
        style={"input_type": "password"},
        write_only=True,
    )
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "password",
            "first_name",
            "last_name",
        ]

    def validate(self, attrs):
        """Validation for password."""
        try:
            password_validation.validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"detail": str(e)})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        # create user record
        user = User.objects.create(**validated_data)
        return user
"""
serializers.py

This module contains Django serializers for user-related functionalities.
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

class UserLoginSerializer(TokenObtainPairSerializer):
    """
    Login serializer for authenticated user.

    Fields:
        - user (UserSerializer)
        - credentials (TokenObtainPairSerializer)
    """

    auth_serializer = UserSerializer  # declare user serializer to be included in login response

    def __init__(self, *args, **kwargs):
        """Overriding to change the error messages."""
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(
            error_messages={
                "blank": "Looks like you submitted wrong data. Please check and try again"
            }
        )
        self.fields["password"] = PasswordField(
            error_messages={
                "blank": "Looks like you submitted wrong data. Please check and try again"
            }
        )

    def validate(self, attrs):
        """Overriding to add user to responses"""
        token_data = super().validate(attrs)

        data = {}
        data["user"] = self.auth_serializer(self.user).data
        data["credentials"] = {**token_data}
        return data

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Fields:
        - email
        - phone_number
        - password
        - first_name
        - last_name
    """

    email = serializers.EmailField(max_length=255, required=True)
    phone_number = PhoneNumberField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=255,
        required=True,
        style={"input_type": "password"},
        write_only=True,
    )
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "password",
            "first_name",
            "last_name",
        ]

    def validate(self, attrs):
        """Validation for password."""
        try:
            password_validation.validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"detail": str(e)})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        # create user record
        user = User.objects.create(**validated_data)
        return user
