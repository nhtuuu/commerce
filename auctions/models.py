from django.contrib.auth.models import AbstractUser
from django.db import models
import locale


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.id} - {self.username}"
    
class Cat(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.id} - {self.name}"
    
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    category = models.CharField(max_length=512, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField(max_length=512, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='won_auctions', null=True, blank=True)
    active = models.BooleanField(default=True)

    def formatted_price(self):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        return locale.currency(self.price, grouping=True)

    def __str__(self):
        return f"{self.id}: {self.title} - {self.description}"

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_items")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def formatted_amount(self):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        return locale.currency(self.amount, grouping=True)

    def __str__(self):
        return f"{self.item} - Bid: ${self.amount} - by {self.bidder}"

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_items")
    comment = models.CharField(max_length=512)
    commenters = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenters}: {self.comment}"

class Watchlist(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_items")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item}"