from django.db import models
import uuid

class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    photo = models.JSONField()  # Storing photo URLs as a JSON array
    location = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    age = models.IntegerField()
    interest = models.JSONField()  # Storing interests as a JSON array
    liked = models.IntegerField(default=0)
    looking_for = models.CharField(max_length=50, choices=[('male', 'Male'), ('female', 'Female')])
    overall = models.IntegerField(default=0)
    bio = models.TextField()
    work = models.CharField(max_length=255)
    edu = models.CharField(max_length=255)
    zodiac = models.CharField(max_length=50)
    isonmatch = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant_addresses = models.JSONField()  # Storing participant addresses

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_id = models.UUIDField()  # Store Chat ID as a UUID
    sender_address = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender_address}: {self.content[:20]}...'
