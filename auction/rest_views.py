from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import AuctionModel
from .serializers import AuctionSerializer


# A simple view. Only define function, not class
@api_view(["GET"])  # Only apply to GET requests
@renderer_classes([JSONRenderer])   # Only return JSON format, not XML or other
def auction_list(request):
    auctions = AuctionModel.objects.all()
    # Serialize auctions
    auctions_serialized = AuctionSerializer(auctions, many=True)
    return Response(auctions_serialized.data)

