from django.shortcuts import render
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

# def index(request):
#     print(request.headers)
#     print("creating response...")
#     html = "<html><body>Hello! <br> <p> This was your request: %s %s <p> sent from the following browser: %s </body></html>" % (request.method, request.path, request.headers['User-Agent'])
#     return HttpResponse(html)


def search(request):
    pass


# If the view is more complex and handles multiple request types then define it using a class
class CreateAuction(View):

    def get(self, request):
        form = CreateAuctionForm()  # Create a blank form
        return render(request, "createauction.html", {"form": form})

    def post(self, request):
        form = CreateAuctionForm(request.POST)   # Create a form with the data the user has POSTed to us
        if form.is_valid():
            cdata = form.cleaned_data
            title = cdata["title"]
            body = cdata["body"]

            auction = AuctionModel(title=title, body=body)  # Create an auction, not saved anywhere yet
            auction.save()  # Save the auction to the database

            return HttpResponseRedirect(reverse("index"))   # Redirect the user after successful auction post
        else:
            return render(request, "createauction.html", {"form": form})    # Give a blank form to the user if the data was not valid



class EditAuction(View):
    pass


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


