import random
import uuid

from django.contrib import messages

from auction.models import AuctionModel
from decimal import *
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone, translation
from user.forms import CustomUserCreationForm
from user.models import UserLanguageModel


def generate_data(request):

    msg_users = "Created users: "
    msg_auctions = "Created auctions: "

    for i in range(100):

        i_str = str(i)

        # CREATE USERS
        user_info = {
            "username": "testUser" + i_str,
            "password": "123",
            "email": "testUser" + i_str + "@mail.com"
        }
        form = CustomUserCreationForm(user_info)

        if form.is_valid():
            new_user = form.save()
            msg_users = msg_users + new_user.username + ', '

            # CREATE USER LANGUAGES
            # Set language
            try:
                language = request.session[translation.LANGUAGE_SESSION_KEY]
            except KeyError:
                language = 'en'
            user_language = UserLanguageModel(user=new_user, language=language)
            user_language.save()

            # CREATE AUCTIONS
            deadline_date = timezone.now() + timezone.timedelta(days=5)
            token = str(uuid.uuid4())  # Unique token for editing without login
            while len(AuctionModel.objects.filter(token=token)) != 0:
                token = str(uuid.uuid4())
            new_auction = AuctionModel(
                title='Title ' + i_str,
                description='Description ' + i_str,
                minimum_price=Decimal(random.randint(1, 100)),
                deadline_date=deadline_date,
                token=token,
                seller=new_user,
                version=1
            )
            new_auction.save()
            msg_auctions = msg_auctions + 'Title ' + i_str + ', '

    messages.add_message(request, messages.INFO, msg_users)
    messages.add_message(request, messages.INFO, msg_auctions)
    messages.add_message(request, messages.INFO, 'Admin users are created using the admin interface (manage.py or django-admin)')

    return redirect(reverse('index'))
