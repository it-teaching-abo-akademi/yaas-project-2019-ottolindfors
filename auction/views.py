import uuid
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import mail
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

    def post(self, request):
        form = CreateAuctionForm(request.POST)   # Create a form with the data the user has POSTed to us
        if form.is_valid():
            cdata = form.cleaned_data
            cdata_is_valid = True

            # Validate minimum price
            if cdata["minimum_price"] < 0.01:
                cdata_is_valid = False
                messages.add_message(request, messages.INFO, "Ensure this value is greater than or equal to 0.01")
            # Validate format of deadline_date (is also done in form)
            try:
                datetime.strftime(cdata["deadline_date"], '%d.%m.%Y %H:%M:%S')
            except ValueError:
                cdata_is_valid = False
                messages.add_message(request, messages.INFO, "Enter a valid date/time")
            # Validate deadline_date
            if cdata["deadline_date"] - timezone.localtime(timezone.now()) < timedelta(hours=72):
                cdata_is_valid = False
                messages.add_message(request, messages.INFO, "The deadline date should be at least 72 hours from now")

            # Create auction or return form
            if cdata_is_valid:
                # TODO: (Addittional) Improve security on user confirmation. According to Dragos L5-Security.pdf
                # Create token unique for editing without login
                token = str(uuid.uuid4())
                while len(AuctionModel.objects.filter(token=token)) != 0:
                    token = str(uuid.uuid4())
                    print('Generated another token: ' + token)
                # Create auction
                new_auction = AuctionModel(
                    title=cdata["title"],
                    description=cdata["description"],
                    minimum_price=cdata["minimum_price"],
                    current_price=cdata["minimum_price"],
                    deadline_date=cdata["deadline_date"],
                    token=token,
                    seller=request.user
                )
                # Save the auction to the database
                new_auction.save()
                # Send a dummy email
                subject = 'Your auction'
                edit_link = '127.0.0.1:8000/auction/edit/no-signin/' + token
                message = 'Auction has been created successfully. Use this link to edit your auction ' + edit_link
                sender = 'bot@erwin.com'
                request.user.email_user(subject=subject, message=message, from_email=sender)
                # Add messages
                messages.add_message(
                    request,
                    messages.INFO,
                    "Auction has been created successfully")
                messages.add_message(
                    request,
                    messages.INFO,
                    "Email has been sent to you. Edit the description of your auction without signin in at " + edit_link)
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
        auctions = AuctionModel.objects.filter(id=id)   # returns an array of matches
        # Only one auction found (as should)
        print(len(auctions))
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
                auction.title = request.POST["title"].strip()
                auction.description = request.POST["description"].strip()
                # save the updated auction
                auction.save()
                messages.add_message(request, messages.INFO, "Auction has been updated successfully")
                return redirect(reverse("index"))
            else:
                messages.add_message(request, messages.INFO, "That is not your auction")
                return redirect(reverse("index"))
        else:
            messages.add_message(request, messages.INFO, "Invalid auction id")
            return redirect(reverse("index"))


class EditAuctionNoSignIn(View):
    def get(self, request, token):
        auctions = AuctionModel.objects.filter(token=token)
        if len(auctions) == 1:
            auction = auctions[0]
            return render(
                request,
                "editauction-no-signin.html",
                {
                    "title": auction.title,
                    "token": auction.token,
                    "description": auction.description
                }
            )
        else:
            messages.add_message(request, messages.INFO, "Invalid auction token")
            return redirect(reverse("index"))

    def post(self, request, token):
        auctions = AuctionModel.objects.filter(token=token)
        if len(auctions) == 1:
            auction = auctions[0]
            auction.description = request.POST.get("description", auction.description).strip()  # no change if failure
            auction.save()
            messages.add_message(request, messages.INFO, "Auction updated successfully")
            return redirect("index")
        else:
            messages.add_message(request, messages.INFO, "Invalid auction token")
            return redirect(reverse("index"))


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


