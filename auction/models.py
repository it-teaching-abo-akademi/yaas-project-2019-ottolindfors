from django.db import models


# Auction model (table)
class AuctionModel(models.Model):
    title = models.CharField(max_length=255)    # Title of the auction
    description = models.TextField()  # Body or description of the auction
    timestamp = models.DateTimeField(auto_now_add=True)

