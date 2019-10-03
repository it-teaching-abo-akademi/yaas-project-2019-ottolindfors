from datetime import datetime

from django.db import models


# Auction model (table)
class AuctionModel(models.Model):
    title = models.CharField(max_length=255)    # Title of the auction
    description = models.TextField()  # Body or description of the auction
    minimum_price = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=datetime.now())  # default=datetime.now()
    status = models.CharField(max_length=1024, default="Active")


# Override default function __str__(self) to print a string presentation of the object instead of memory address
def __str__(self):
    return self.title

