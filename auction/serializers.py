from rest_framework import serializers
from .models import AuctionModel


# Serialises the data from the AuctionModel
class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionModel    # The model to serialize
        fields = ("id", "title")    # The fields  from the model to serialize
