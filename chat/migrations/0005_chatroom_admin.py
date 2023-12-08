# Generated by Django 3.2.18 on 2023-12-06 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_auto_20231206_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chatroom_admin', to=settings.AUTH_USER_MODEL),
        ),
    ]
