from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
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
    if (request.GET.get("title") != "") or (request.GET.get("id") != ""):  # Search by title and/or id
        print("IF\n" + str(request.GET))
        criteria = request.GET["title"].lower().strip()
        searchid = request.GET["id"].lower().strip()
        search_result = AuctionModel.objects.filter(title__contains=criteria, id__contains=searchid, status="Active").order_by('deadline_date')
    else:
        print("ELSE\n" + str(request.GET))
        search_result = AuctionModel.objects.filter(status="Active").order_by('-timestamp')
    return render(request, "index.html", {"auctions": search_result})


@method_decorator(login_required, name='dispatch')
class CreateAuction(View):
    def get(self, request):
        form = CreateAuctionForm()  # Create a blank form
        return render(request, "createauction.html", {"form": form})

    def post(self, request):
        form = CreateAuctionForm(request.POST)   # Create a form with the data the user has POSTed to us
        if form.is_valid():
            cdata = form.cleaned_data
            new_auction = AuctionModel(title=cdata["title"],
                                   description=cdata["description"],
                                   minimum_price=cdata["minimum_price"],
                                   deadline_date=cdata["deadline_date"])  # Create an auction, not saved anywhere yet
            new_auction.save()  # Save the auction to the database

            messages.add_message(request, messages.INFO, "Your auction was successfully added")
            return HttpResponseRedirect(reverse("index"))   # Redirect the user after successful auction post
        else:
            messages.add_message(request, messages.INFO, "We tried everything. Looks like the data you gave us was "
                                                         "invalid.")
            return render(request, "createauction.html", {"form": form})  # Give a blank form to the user if the data was not valid


@method_decorator(login_required, name='dispatch')
class EditAuction(View):
    def get(self, request, id):
        auctions = AuctionModel.objects.filter(id=id)   # returns an array of matches
        ''' auction = get_object_or_404(AuctionModel, id=id) '''
        if len(auctions) == 1:
            auction = auctions[0]
            # return the pre-filled form to the user for editing
            return render(request, "editauction.html", {"user": request.user,
                                                        "title": auction.title,
                                                        "id": auction.id,
                                                        "description": auction.description,
                                                        "deadline_date": auction.deadline_date,
                                                        "minimum_price": auction.minimum_price,
                                                        "status": auction.status})  # add {{max_lentgh}}
        else:
            messages.add_message(request, messages.INFO, "Invalid auction id")
            return HttpResponseRedirect(reverse("auction:index"))

    def post(self, request, id):
        auctions = AuctionModel.objects.filter(id=id)   # returns an array of matches
        if len(auctions) == 1:
            auction = auctions[0]
        else:
            messages.add_message(request, messages.INFO, "Invalid auction id")
            return HttpResponseRedirect(reverse("auction:index"))

        title = request.POST["title"].strip()   # get the title from the posted data
        description = request.POST["description"].strip()  # get the description from the posted data
        auction.title = title
        auction.description = description
        auction.save()  # save the updated auction

        messages.add_message(request, messages.INFO, "Auction updated")
        return HttpResponseRedirect(reverse("auction:index"))


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


