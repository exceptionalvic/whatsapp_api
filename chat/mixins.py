"""Mixins reusable accross models."""
from django.db import models


class TimeStampMixin(models.Model):
    """Add date created_at and date updated_at to models"""

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
