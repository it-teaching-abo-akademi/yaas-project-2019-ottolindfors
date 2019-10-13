from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from auction.models import AuctionModel
from auction.serializers import AuctionSerializer


class BrowseAuctionApi(APIView):
    pass

# @renderer_classes([JSONRenderer])   # Only return JSON format, not XML or other
# class BrowseAuctionApi(APIView):
#     def get(self, request):
#         auctions = AuctionModel.objects.all()
#         auctions_serialized = AuctionSerializer(auctions, many=True)
#         return Response(auctions_serialized.data)
#
#     def post(self, request):
#         pass


class SearchAuctionApi(APIView):
    pass


class SearchAuctionWithTermApi(APIView):
    pass


class SearchAuctionApiById(APIView):
    pass


class BidAuctionApi(APIView):
    pass
