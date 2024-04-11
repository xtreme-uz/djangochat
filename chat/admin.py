from django.contrib import admin

from chat.models import Chat, ChatMember, Message

admin.site.register(Chat)
admin.site.register(ChatMember)
admin.site.register(Message)
