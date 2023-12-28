from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=500, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    likers = models.ManyToManyField(User, related_name="liked_posts")