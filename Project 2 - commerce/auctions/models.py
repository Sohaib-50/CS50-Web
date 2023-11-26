from django.contrib.auth.models import AbstractUser
from django.db import models


class Listing(models.Model):
    lister = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)


class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchers")


class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
        

class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)