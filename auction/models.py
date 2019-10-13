from datetime import datetime

from django.conf import settings
from django.db import models


# Auction model (table)
class AuctionModel(models.Model):
    title = models.CharField(max_length=255)    # Title of the auction
    description = models.TextField()  # Body or description of the auction
    minimum_price = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(default=datetime.now)  # default=datetime.now()
    status = models.CharField(max_length=1024, default="Active")
    token = models.CharField(max_length=255, unique=True, null=True)
    # ForeignKey references the currently active User model (CustomUser) via settings.AUTH_USER_MODEL
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # seller = models.ForeignKey(SellerUserMap, on_delete=models.PROTECT)


# Override default function __str__(self) to print a string presentation of the object instead of memory address
def __str__(self):
    return self.title

