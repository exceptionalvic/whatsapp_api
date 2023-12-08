# Generated by Django 3.2.18 on 2023-12-05 14:25

import chat.entity.chat_models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('attachment', models.FileField(blank=True, max_length=455, null=True, upload_to=chat.entity.chat_models.attachment_location)),
                ('chat_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatroom')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]