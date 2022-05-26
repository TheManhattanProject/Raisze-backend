from django.db import models
from users.models import CustomUser
# Create your models here.


class ChatRoom(models.Model):
    chat_id = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(CustomUser)


class Message(models.Model):
    text = models.TextField()
    chatroom = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages')
