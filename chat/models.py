from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)


class ChatMember(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='members')
    member_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['chat_id', 'member_id']


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        ordering = ['created']
