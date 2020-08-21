from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    imageLink = models.CharField(max_length=200, blank=True, default=None, null=True)
    uploadDate = models.DateTimeField()
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listedBy")
    watched = models.ManyToManyField(User, blank=True, related_name="watching")
    currentbid = models.ForeignKey('Bids',on_delete=models.DO_NOTHING, null=True, blank=True, related_name="currentbid")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name="categorize", blank=True, default=None, null=True)
    active = models.BooleanField(default=True)

class Bids(models.Model):
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bided")
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    amount = models.DecimalField(max_digits=10,decimal_places=2) 

class Comments(models.Model):
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented")
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField()

class Category(models.Model):
    title = models.CharField(max_length=64)    