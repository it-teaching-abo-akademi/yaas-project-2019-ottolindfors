from django.contrib.auth.decorators import login_required
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from auction.models import AuctionModel
from auction.serializers import AuctionSerializer


@renderer_classes([JSONRenderer])
class BrowseAuctionApi(APIView):
    def get(self, request):
        auctions = AuctionModel.objects.filter(status='Active')
        # Serialize auctions
        auctions_serialized = AuctionSerializer(auctions, many=True)
        return Response(auctions_serialized.data)


class SearchAuctionApi(APIView):
    pass


@renderer_classes([JSONRenderer])
class SearchAuctionWithTermApi(APIView):
    pass


class SearchAuctionApiById(APIView):
    pass


@login_required
class BidAuctionApi(APIView):
    pass
