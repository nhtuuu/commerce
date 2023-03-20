from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    category = models.CharField(max_length=64)
    price = models.IntegerField()
    url = models.URLField(max_length=512, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.title} - {self.description} - ${self.price}"

class Bid(models.Model):
    bidder = models.CharField(max_length=64)
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment = models.CharField(max_length=512)
    commenters = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item}"
