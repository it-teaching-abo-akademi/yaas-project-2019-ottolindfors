from django.http import JsonResponse
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from auction.models import AuctionModel
from auction.serializers import AuctionSerializer


@renderer_classes([JSONRenderer])
class BrowseAuctionApi(APIView):
    def get(self, request):
        # Get all auctions
        auctions = AuctionModel.objects.filter(status='Active')
        auctions_serialized = AuctionSerializer(auctions, many=True)
        return Response(auctions_serialized.data)


@renderer_classes([JSONRenderer])
class SearchAuctionApi(APIView):
    def get(self, request, title):
        auctions = AuctionModel.objects.filter(status='Active', title__contains=title)
        auctions_serialized = AuctionSerializer(auctions, many=True)
        return Response(auctions_serialized.data)


@renderer_classes([JSONRenderer])
class SearchAuctionWithTermApi(APIView):
    def get(self, request):
        if request.GET.get('term', '') != '':
            # Get auctions that match the search term
            term = request.GET['term'].lower().strip()
            auctions = AuctionModel.objects.filter(status='Active', title__contains=term)
            auctions_serialized = AuctionSerializer(auctions, many=True)
            return Response(auctions_serialized.data)
        else:
            # Get all auctions
            auctions = AuctionModel.objects.filter(status='Active')
            auctions_serialized = AuctionSerializer(auctions, many=True)
            return Response(auctions_serialized.data)


@renderer_classes([JSONRenderer])
class SearchAuctionApiById(APIView):
    def get(self, request, auction_id):
        # Get the auction with matching id. If none is found .filter() returns empty query set
        if AuctionModel.objects.filter(id=auction_id).exists() and AuctionModel.objects.filter(id=auction_id, status='Active'):
            auction = AuctionModel.objects.get(id=auction_id)
            auction_serialized = AuctionSerializer(auction)
            return Response(auction_serialized.data)
        else:
            error_dict = {
                'result': 'Empty',
                'message': 'No active auctions with id=' + str(auction_id) + ' found.'
            }
            return JsonResponse(error_dict)


class BidAuctionApi(APIView):
    pass
