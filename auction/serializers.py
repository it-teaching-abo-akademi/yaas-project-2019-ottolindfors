from rest_framework import serializers
from .models import AuctionModel


# Serialises the data from the AuctionModel
class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionModel    # The model to serialize
        fields = ("title", "description", "minimum_price", "deadline_date")    # The fields  from the model to serialize


class BidAPIAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionModel    # The model to serialize
        fields = ("title", "description", "current_price", "deadline_date")    # The fields  from the model to serialize
