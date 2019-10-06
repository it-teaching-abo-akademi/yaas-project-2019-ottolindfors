from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


# Auction model (table)
class AuctionModel(models.Model):
    title = models.CharField(max_length=255)    # Title of the auction
    description = models.TextField()  # Body or description of the auction
    minimum_price = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField()  # was default=datetime.now()
    status = models.CharField(max_length=1024, default="Active")
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # seller = models.ForeignKey(SellerUserMap, on_delete=models.PROTECT)
    '''
    By default the AuctionModel instance (an auction) would be deleted if the User (seller) is deleted. To prevent this
    the on_delete is set to null by on_delete=models.SET_NULL.

    With GDPR in mind the foreign key should not be the User. Instead it could be a integer/hash in a table that maps
    integers to users. If a user is deleted admins can still see the items sold by the same user but the username will 
    not be avalible anymore.

    Example: 
    AuctionModel(seller_id, ...)
    SellerUserMap(seller_id, username)
    User(username, ...)

    Before deletion of a user the auction is shown with the seller as 'username'.
    After deletion of a user the auction is shown with the seller as 'username'. Only admins can see the auctions.
    '''


# Override default function __str__(self) to print a string presentation of the object instead of memory address
def __str__(self):
    return self.title

class Bid(models.Model):
    # An auction should not be deleted but on_delete=SET_NULL just in case
    auction = models.ForeignKey(AuctionModel, on_delete=models.SET_NULL, null=True)
    bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)