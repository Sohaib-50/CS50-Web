from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers")
    
    def serialize(self):
        return {
            "username": self.username,
            "followers_count": self.followers.count(),
            "following_count": self.following.count(),
        }


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=500, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    likers = models.ManyToManyField(User, related_name="liked_posts")   

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likers.count(),
        }