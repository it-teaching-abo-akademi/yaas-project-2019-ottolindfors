from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from auction import views
from auction.forms import BidForm
from auction.models import AuctionModel
from auction.serializers import AuctionSerializer, BidAPIAuctionSerializer


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
                'message': 'No active auctions with id=' + str(auction_id) + ' found.'
            }
            return JsonResponse(error_dict)


@renderer_classes([JSONRenderer])
class BidAuctionApi(APIView):
    def post(self, request, item_id):
        # TODO: using is_authenticated is not good since it does not check if user is banned etc.
        if request.user.is_authenticated:
            try:
                # Try to parse the int
                post_data = {'new_price': int(request.POST['new_price'])}

                form = BidForm(post_data)
                if form.is_valid():
                    result_dict = views.do_bid(request, item_id)
                    status = result_dict['status']
                    msg = result_dict['msg']

                    if status == 'success':
                        # This is correct. Test pass.
                        auction = AuctionModel.objects.get(id=item_id)
                        data = BidAPIAuctionSerializer(auction).data
                        data.update({'message': 'Bid successfully'})
                        return Response(data)
                    elif status == 'fail-redirect-to-index':
                        pass
                    elif status == 'fail-rerender':
                        return Response({'message': msg}, status=400)
                    else:
                        msg = msg + '. Unexpected error'
                        return Response({'message': msg}, status=400)
                else:
                    response_dict = {'message': 'Invalid form data'}
                    return Response(response_dict)

            except ValueError:
                msg = 'Bid must be a number'
                return Response({'message': msg}, status=400)
        else:
            response_dict = {'detail': 'Authentication credentials were not provided'}
            return Response(response_dict, status=401)
