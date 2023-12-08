"""
jwt_auth_middleware.py

This module defines a Django Channels middleware for 
handling JWT authentication.
"""

import traceback
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import decode as jwt_decode

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

class JWTAuthAsyncMiddleware:
    """
    Middleware for JWT authentication in Django Channels.

    Attributes:
        app: The application to be wrapped by this middleware.

    Methods:
        __call__: Method to call the middleware.
        get_payload: Method to decode the JWT token and get the payload.
        get_user_credentials: Method to get user credentials from the JWT token payload.
        get_logged_in_user: Method to get the logged-in user.
        get_user: Method to get a user by ID.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Close any existing database connections to prevent potential thread leakage
        close_old_connections()

        # Check if the authorization header is present
        auth_header_exists_mapped_list = list(
            map(lambda header: header[0] == b"authorization", scope["headers"])
        )

        # Get the token
        if any(auth_header_exists_mapped_list):
            for header in scope["headers"]:
                if header[0] == b"authorization":
                    tk = header[1].decode().split(" ")[1]
                    header_parsed = parse_qs(f"{header[0].decode()}={tk}")
                    token = header_parsed.get("authorization", None)
                    break
        elif "token" in parse_qs(scope["query_string"].decode("utf8")):
            token = parse_qs(scope["query_string"].decode("utf8")).get(
                "token", None
            )
        else:
            token = None

        if token is not None:
            token = token[0]
        else:
            raise ValueError("Token not found in query params")

        try:
            # This will automatically validate the token 
            # and raise an error if the token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            return None
        else:
            # Token is valid, decode it
            decoded_data = self.get_payload(token)

            # Get the user id from decoded data
            user_id = self.get_user_credentials(decoded_data)

            # Get the user using ID
            scope["user"] = await self.get_user(user_id=user_id)

        # Call the wrapped application
        return await self.app(scope, receive, send)

    def get_payload(self, jwt_token):
        """
        Decode the JWT token and get the payload.

        Args:
            jwt_token (str): The JWT token.

        Returns:
            dict: The decoded payload.
        """
        payload = jwt_decode(
            jwt_token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        return payload

    def get_user_credentials(self, payload):
        """
        Get user credentials from the JWT token payload.

        Args:
            payload (dict): The JWT token payload.

        Returns:
            Any: The user credentials, defaults to user id.
        """
        user_id = payload["user_id"]
        return user_id

    async def get_logged_in_user(self, user_id):
        """
        Get the logged-in user.

        Args:
            user_id: The ID of the user.

        Returns:
            User: The logged-in user.
        """
        user = await self.get_user(user_id)
        return user

    @database_sync_to_async
    def get_user(self, user_id):
        """
        Get a user by ID.

        Args:
            user_id: The ID of the user.

        Returns:
            User: The user object.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()

def JWTAuthMiddlewareStack(app):
    """
    Wrapper function for the JWTAuthAsyncMiddleware, 
    which is used to wrap the Django Channels application.

    Args:
        app: The Django Channels application.

    Returns:
        JWTAuthAsyncMiddleware: The wrapped application with 
        JWT authentication middleware.
    """
    return JWTAuthAsyncMiddleware(AuthMiddlewareStack(app))
