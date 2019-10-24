from datetime import datetime

from django.conf import settings
from django.db import models


# Auction model (table)
from django.db.models import Max


class AuctionModel(models.Model):
    title = models.CharField(max_length=255)    # Title of the auction
    description = models.TextField()  # Body or description of the auction
    minimum_price = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)  # allow up to 1 000 000 000 000.00
    timestamp = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(default=datetime.now)  # default=datetime.now()
    status = models.CharField(max_length=1024, default="Active")  # Active, Banned, Due, Adjudicated
    token = models.CharField(max_length=255, unique=True, null=True)
    # Many auctions can refer to the same seller (one seller can have many auctions)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    version = models.IntegerField(default=1)

    @property
    def current_price(self):
        query_set_max_price = BidModel.objects.filter(auction=self).aggregate(Max('new_price'))
        current_price = query_set_max_price.get('new_price__max')
        if current_price is None:
            current_price = self.minimum_price
        return round(current_price, 2)  # only two decimals

    def get_winning_bid(self):
        return BidModel.objects.filter(auction=self, new_price=self.current_price)

    def get_winning_bidder(self):
        return BidModel.objects.filter(auction=self, new_price=self.current_price).buyer

    def get_second_place_bidder(self):
        # TODO: Fix error when index out of range (may some sort of .get() instead of [1])
        try:
            # bidder = BidModel.objects.filter(auction=self).order_by('-new_price')[1].buyer
            bidder = BidModel.objects.get(auction=self, new_price=self.current_price).buyer
        except IndexError:
            bidder = None
            # TODO: Handle this None return in auction:bid function
        return bidder

    def increment_version(self):
        self.version += 1

    @property
    def next_version_number(self):
        return self.version + 1

    # Override default function __str__(self) to print a string presentation of the object instead of memory address
    def __str__(self):
        return self.title


class BidModel(models.Model):
    # Many bids can refer to the same auction (One auction can have many bids)
    auction = models.ForeignKey(AuctionModel, on_delete=models.PROTECT)
    # Many bids can refer to the same buyer
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    new_price = models.DecimalField(decimal_places=2, max_digits=15, default=0.00)  # allow up to 1 000 000 000 000.00

    @property
    def get_min_bid_amount(self):
        query_set_max_price = BidModel.objects.filter(auction=self.auction).aggregate(Max('new_price'))
        min_bid = query_set_max_price.get('new_price') + 1
        pass

    #
    # def save(self):
    #     pass

