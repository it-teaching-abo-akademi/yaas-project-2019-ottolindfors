from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, request, HttpResponseRedirect
from django.urls import reverse
from .models import AuctionModel
from .forms import CreateAuctionForm


# If the view is simple and handling only one request type then it is okay to define it using a function
def index(request):
    auctions = AuctionModel.objects.all()
    print(auctions)  # debugging
    return render(request, "index.html", {"auctions": auctions})


'''
def index(request):
    print(request.headers)
    print("creating response...")
    html = "<html><body>Hello! <br> <p> This was your request: %s %s <p> sent from the following browser: %s </body></html>" % (request.method, request.path, request.headers['User-Agent'])
    return HttpResponse(html)
'''


def search(request):
    pass


# If the view is more complex and handles multiple request types then define it using a class
@method_decorator(login_required, name='dispatch')
class CreateAuction(View):
    def get(self, request):
        form = CreateAuctionForm()  # Create a blank form
        return render(request, "createauction.html", {"form": form})

    def post(self, request):
        form = CreateAuctionForm(request.POST)   # Create a form with the data the user has POSTed to us
        if form.is_valid():
            cdata = form.cleaned_data
            title = cdata["title"]
            description = cdata["description"]

            auction = AuctionModel(title=title, description=description)  # Create an auction, not saved anywhere yet
            auction.save()                                  # Save the auction to the database

            messages.add_message(request, messages.INFO, "Your auction was successfully added")
            return HttpResponseRedirect(reverse("index"))   # Redirect the user after successful auction post
        else:
            messages.add_message(request, messages.INFO, "We tried everything. Looks like the data you gave us was "
                                                         "invalid.")  # eBay style error message
            return render(request, "createauction.html", {"form": form})    # Give a blank form to the user if the data was not valid


@method_decorator(login_required, name='dispatch')
class EditAuction(View):
    def get(self, request, id):
        auctions = AuctionModel.objects.filter(id=id)   # returns an array of matches
        ''' auction = get_object_or_404(AuctionModel, id=id) '''
        if len(auctions) == 1:
            auction = auctions[0]
            # return the pre-filled form to the user for editing
            return render(request, "editauction.html", {"user": request.user, "title": auction.title, "id": auction.id,
                                                        "description": auction.description})  # add {{max_lentgh}}
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


