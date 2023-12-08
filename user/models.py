# your_app_name/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
import uuid
from chat.mixins import TimeStampMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, TimeStampMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        _("First Name"), max_length=150, null=True, blank=True
    )
    last_name = models.CharField(
        _("Last Name"), max_length=150, null=True, blank=True
    )
    username = models.CharField(
        help_text="Username",
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        help_text="User's Phone Number", unique=False, null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            # generate a random unique username
            self.username = (
                self.email.split("@")[0]
                + "_"
                + str(uuid.uuid4()).split("-")[-1]
            )
        super(User, self).save(*args, **kwargs)
