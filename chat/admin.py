from django.contrib import admin
from .models import ChatRoom, Message

admin.site.register(ChatRoom, admin.ModelAdmin)
admin.site.register(Message, admin.ModelAdmin)

# Register your models here.
