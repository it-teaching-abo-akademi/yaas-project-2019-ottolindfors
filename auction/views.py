from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, request, HttpResponseRedirect
from django.urls import reverse

from .models import AuctionModel
from .forms import CreateAuctionForm


def index(request):
    auctions = AuctionModel.objects.filter(status='Active').order_by('deadline_date')  # nearest deadline first
    print(auctions)  # debugging
    return render(request, "index.html", {"auctions": auctions})


def search(request):
    # TODO: return search results as json? See commented below
    if request.GET.get("term") != "":  # search by title
        print("IF\n" + str(request.GET))
        criteria = request.GET["term"].lower().strip()
        search_result = AuctionModel.objects.filter(title__contains=criteria, status="Active").order_by('deadline_date')
    else:
        print("ELSE\n" + str(request.GET))
        search_result = AuctionModel.objects.filter(status="Active").order_by('-timestamp')
    return render(request, "index.html", {"auctions": search_result})


"""
# Returning JSON search result does not pass test
@api_view(["GET"])  # Only apply to GET requests
@renderer_classes([JSONRenderer])   # Only return JSON format, not XML or other
def search(request):
    if request.GET.get("term") != "":
        print("IF\n" + str(request.GET))  # debugging
        criteria = request.GET["term"].lower().strip()
        # Search result
        auctions = AuctionModel.objects.filter(title__contains=criteria, status="Active").order_by('deadline_date')
        # Serialize data
        auctions_serialized = AuctionSerializer(auctions, many=True)
        return Response(auctions_serialized.data)
    else:
        pass
"""


@method_decorator(login_required, name='dispatch')
class CreateAuction(View):
    def get(self, request):
        form = CreateAuctionForm()  # Create a blank form
        return render(request, "createauction.html", {"form": form})

    # TODO: Check minimum price.
    def post(self, request):
        form = CreateAuctionForm(request.POST)   # Create a form with the data the user has POSTed to us
        if form.is_valid():
            print("here")
            cdata = form.cleaned_data
            minimum_price = cdata["minimum_price"]
            deadline_date = cdata["deadline_date"]

            cdata_is_valid = True

            # Validate minimum price
            if minimum_price < 0.01:
                cdata_is_valid = False
                messages.add_message(request, messages.INFO, "Ensure this value is greater than or equal to 0.01")

            # Validate format of deadline_date
            try:
                datetime.strftime(deadline_date, '%d.%m.%Y %H:%M:%S')
            except ValueError:
                cdata_is_valid = False
                messages.add_message(request, messages.INFO, "Enter a valid date/time")

            # Validate deadline_date
            t1 = deadline_date
            t2 = timezone.localtime(timezone.now())
            if t1-t2 < timedelta(hours=72):
                cdata_is_valid = False
                messages.add_message(request, messages.INFO, "The deadline date should be at least 72 hours from now")

            # Create auction or return form
            if cdata_is_valid:
                seller = request.user
                new_auction = AuctionModel(
                    title=cdata["title"],
                    description=cdata["description"],
                    minimum_price=cdata["minimum_price"],
                    deadline_date=cdata["deadline_date"],
                    seller=seller
                )

                # Save the auction to the database
                new_auction.save()

                messages.add_message(request, messages.INFO, "Auction has been created successfully")
                return redirect('index')
            else:
                messages.add_message(request, messages.INFO, "Please check your entries")
                return render(request, "createauction.html", {"form": form})

        else:
            messages.add_message(
                request,
                messages.INFO,
                "We tried everything. Looks like the data you gave us was invalid."
            )
            return render(request, "createauction.html", {"form": form})  # Give a blank form to the user if the data was not valid


@method_decorator(login_required, name='dispatch')
class EditAuction(View):
    def get(self, request, id):
        # TODO: Users can only get their own auctions
        auctions = AuctionModel.objects.filter(id=id)   # returns an array of matches

        # Only one auction found (as should)
        if len(auctions) == 1:
            auction = auctions[0]

            # Check ownership of auction
            # Must use username since they are both the same type (str)
            if request.user.username == auction.seller.username:
                # return the pre-filled form to the user for editing
                return render(
                    request,
                    "editauction.html",
                    {
                        "user": request.user,
                        "title": auction.title,
                        "id": auction.id,
                        "description": auction.description,
                        "deadline_date": auction.deadline_date,
                        "minimum_price": auction.minimum_price,
                        "status": auction.status
                    }
                )
            else:
                messages.add_message(request, messages.INFO, "That is not your auction to edit")
                return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.INFO, "Invalid auction id")
            return HttpResponseRedirect(reverse("index"))

    def post(self, request, id):
        auctions = AuctionModel.objects.filter(id=id)   # returns an array of matches
        if len(auctions) == 1:
            auction = auctions[0]

            # Check ownership of auction
            # Must use username since they are both the same type (str)
            if request.user.username == auction.seller.username:
                title = request.POST["title"].strip()  # get the title from the posted data
                description = request.POST["description"].strip()  # get the description from the posted data
                auction.title = title
                auction.description = description

                auction.save()  # save the updated auction

                messages.add_message(request, messages.INFO, "Auction has been updated successfully")
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.add_message(request, messages.INFO, "That is not your auction")
                return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.INFO, "Invalid auction id")
            return HttpResponseRedirect(reverse("index"))


def bid(request, item_id):
    pass


def ban(request, item_id):
    pass


def resolve(request):
    pass


def changeLanguage(request, lang_code):
    pass


def changeCurrency(request, currency_code):
    pass


