from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.forms import UserCreationForm


class SignUp(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()  # Everything is handled by UserCreationForm. No need to implement database ourselves

            messages.add_message(request, messages.INFO, "User created")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.INFO, "Please check that you use valid characters")
            return render(request, "signup.html", {"form": form})


class SignIn(View):
    def get(self, request):
        return render(request, "signin.html")

    def post(self, request):
        username = request.POST.get('username', '')  # Empty '' tells the get method to return '' if username not found
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)
        # If no user is found
        if user is None:
            messages.add_message(request, messages.INFO, "Invalid username or password")
            return render(request, "signin.html")
        # Else some user is found and we want to let the user login with the given credidentials
        else:
            auth.login(request, user)
            messages.add_message(request, messages.INFO, "Welcome! Signed in.")
            return HttpResponseRedirect(reverse("index"))


@login_required
def signout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "Signed out.")
    return HttpResponseRedirect(reverse("index"))


class EditProfile(View):
    pass
