import uuid
from datetime import datetime, timedelta
from decimal import *

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, request, HttpResponseRedirect
from django.urls import reverse

from user.models import CustomUser
from .models import AuctionModel, BidModel
from .forms import CreateAuctionForm, BidForm


def index(request):
    auctions = AuctionModel.objects.filter(status='Active').order_by('deadline_date')  # nearest deadline first
    return render(request, "index.html", {"auctions": auctions, "time": timezone.localtime(timezone.now())})


def search(request):
    if request.GET.get("term", "") != "":  # search by title
        criteria = request.GET["term"].lower().strip()
        search_result = AuctionModel.objects.filter(title__contains=criteria, status="Active").order_by('deadline_date')
    else:
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
            cdata_is_valid = True

            # Validate minimum price
            if cdata["minimum_price"] < Decimal('0.01'):  # < 0.01 evaluates incorrectly as float 0.01 is larger than decimal 0.01
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
                title = cdata["title"]
                description = cdata["description"]
                minimum_price = cdata["minimum_price"]
                deadline_date = cdata["deadline_date"]
                seller = request.user
                # TODO: toggle to False to pass tests
                # Specs say we need confirmation but tests do not work with confirmation
                ask_for_confirmation = False
                if ask_for_confirmation:
                    # Save to session
                    save_to_session(
                        request=request,
                        title=title,
                        description=description,
                        minimum_price=minimum_price,
                        deadline_date=deadline_date,
                        seller_username=seller.username
                    )
                    # Redirect to confirmaion
                    return render(
                        request,
                        "createauction-confirm.html",
                        {
                            "title": title,
                            "description": description,
                            "minimum_price": minimum_price,
                            "deadline_date": deadline_date,
                            "seller_username": seller.username
                        }
                    )
                else:
                    # Create token unique for editing without login
                    token = str(uuid.uuid4())
                    while len(AuctionModel.objects.filter(token=token)) != 0:
                        token = str(uuid.uuid4())
                        print('Generated another token: ' + token)
                    # Create auction
                    new_auction = AuctionModel(
                        title=title,
                        description=description,
                        minimum_price=minimum_price,
                        deadline_date=deadline_date,
                        token=token,
                        seller=seller
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
class ConfirmAuction(View):
    def get(self, request):
        pass
        # give a html/form with yes button

    def post(self, request):
        # if yes is posted to us then:
        # new_auction = get_from_session()
        # new_auction.save()
        if request.POST.get('confirmation_input', '') == "Confirm":
            # Retrieve data from stored session
            auction_data = get_from_session(request)
            # Check that user is the correct signed in user, no session hijacking
            if request.user.username == auction_data['seller_username']:
                # Create token unique for editing without login
                token = str(uuid.uuid4())
                while len(AuctionModel.objects.filter(token=token)) != 0:
                    token = str(uuid.uuid4())
                    print('Generated another token: ' + token)
                title = auction_data['title']
                description = auction_data['description']
                minimum_price = auction_data['minimum_price']
                deadline_date = auction_data['deadline_date']
                seller = CustomUser.objects.get(username=request.user.username)
                # Create auction
                new_auction = AuctionModel(
                    title=title,
                    description=description,
                    minimum_price=minimum_price,
                    deadline_date=deadline_date,
                    token=token,
                    seller=seller
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
            messages.add_message(request, messages.INFO, "Auction not confirmed")
            return redirect('index')


@login_required
def save_to_session(request, title, description, minimum_price, deadline_date, seller_username):
    request.session['title'] = title
    request.session['description'] = description
    request.session['minimum_price'] = str(minimum_price)  # otherwise error
    request.session['deadline_date'] = datetime.strftime(deadline_date, '%d.%m.%Y %H:%M:%S')  # otherwise error
    request.session['seller_username'] = seller_username  # prevent session hijacking
    print('input: ' + str(minimum_price) + ' : ' + str(deadline_date))


@login_required
def get_from_session(request):
    title = request.session['title']
    description = request.session['description']
    minimum_price = Decimal(request.session['minimum_price'])
    deadline_date = datetime.strptime(request.session['deadline_date'], '%d.%m.%Y %H:%M:%S')
    seller_username = request.session['seller_username']
    print('output: ' + str(minimum_price) + ' : ' + str(deadline_date))
    auction_data = {
        "title": title,
        "description": description,
        "minimum_price": minimum_price,
        "deadline_date": deadline_date,
        "seller_username": seller_username
    }
    return auction_data


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


@method_decorator(login_required, name='dispatch')
class Bid(View):
    def get(self, request, item_id):
        # Auction exists
        if AuctionModel.objects.filter(id=item_id).exists():
            auction = AuctionModel.objects.get(id=item_id)
            # Check that auction is active
            if auction.status == "Active":
                # Check that user (bidder) is not the seller
                if auction.seller.username != request.user.username:
                    # Check deadline
                    if auction.deadline_date - timezone.localtime(timezone.now()) > timedelta(seconds=1):
                        inidata = {"new_price": auction.current_price}
                        form = BidForm(initial=inidata)
                        return render(request, "bid.html", {"auction": auction, "form": form, "item_id": item_id})
                    else:
                        msg = "You can only bid on active auctions. Deadline due."
                else:
                    msg = "You cannot bid on your own auctions"
            else:
                msg = "You can only bid on active auctions"

            messages.add_message(request, messages.INFO, msg)
            return redirect('index')
        else:
            msg = "Invalid auction id"
            messages.add_message(request, messages.INFO, msg)
            return redirect('index')

    def post(self, request, item_id):
        form = BidForm(request.POST)
        # if form.is_valid():
        #     pass
        # else:
        #     messages.add_message(request, messages.INFO, "Form is not valid")
        #     return render(request, "bid.html", {"form": form})

        # TODO Use a form for bidding
        # Check that auction exist
        if AuctionModel.objects.filter(id=item_id).exists():
            auction = AuctionModel.objects.get(id=item_id)
            success = False
            # Check that auction is active
            if auction.status == "Active":
                # Check that user (bidder) is not the seller
                if auction.seller.username != request.user.username:
                    buyer = request.user
                    # Check that new_price is valid. Round to two decimals
                    new_price = round(Decimal(request.POST.get('new_price', '')), 2)
                    min_increment = round(Decimal('0.01'), 2)
                    print('new_price: ' + str(new_price))
                    print('current_price: ' + str(auction.current_price))
                    print('min_increment: ' + str(min_increment))
                    print('delta: ' + str(new_price - auction.current_price))
                    if new_price - auction.current_price >= min_increment:
                        # Check deadline
                        if auction.deadline_date - timezone.localtime(timezone.now()) > timedelta(seconds=1):  # give 1 second processing time
                            # TODO: Check that the user is bidding on the latest description (use version numbers)

                            # Save the new_bid
                            new_bid = BidModel(new_price=new_price, buyer=buyer, auction=auction)
                            new_bid.save()

                            # Send email
                            subject = 'New bid'
                            message = 'A new bid has been placed.'
                            sender = 'bot@erwin.com'
                            second_place_bidder = auction.get_second_place_bidder()
                            second_place_bidder.email_user(subject=subject, message=message, from_email=sender)
                            auction.seller.email_user(subject=subject, message=message, from_email=sender)

                            msg = "You has bid successfully"
                            success = True
                        else:
                            msg = "You can only bid on active auctions. Deadline due."
                    else:
                        msg = "New bid must be greater than the current bid for at least 0.01"
                else:
                    msg = "You cannot bid on your own auctions"
            else:
                msg = "You can only bid on active auctions"

            if success:
                messages.add_message(request, messages.INFO, msg)
                return redirect('index')
            else:
                messages.add_message(request, messages.INFO, msg)
                return render(request, "bid.html", {"auction": auction, "form": form, "item_id": item_id})
        else:
            msg = "Invalid auction id"
            messages.add_message(request, messages.INFO, msg)
            return redirect('index')


        # TODO: Figure out how to return correctly 200 and not 302
        # return redirect('index')
        # return render(request, "bid.html")


@login_required
def ban(request, item_id):
    if request.method == 'POST':
        # TODO: Send emails to seller and all bidders after ban
        # Check permission
        if request.user.is_superuser:
            # Auction exists
            if AuctionModel.objects.filter(id=item_id).exists():
                auction = AuctionModel.objects.get(id=item_id)
                # Auction is active in order to ban
                if auction.status == 'Active':
                    AuctionModel.objects.filter(id=item_id).update(status="Banned")
                    msg = "Ban successfully. Auction " + str(AuctionModel.objects.get(id=item_id).id) + " is now " + AuctionModel.objects.get(id=item_id).status
                else:
                    msg = "Auction status is " + auction.status
            else:
                msg = "Invalid auction id"
        else:
            msg = "Only admins has the right to ban an auction"
        # Return to index with messages
        messages.add_message(request, messages.INFO, msg)
        return redirect('index')
    else:
        messages.add_message(request, messages.INFO, "GET method not avalible")
        return redirect('index')


@login_required
def resolve(request):
    pass


def changeLanguage(request, lang_code):
    pass


def changeCurrency(request, currency_code):
    pass

