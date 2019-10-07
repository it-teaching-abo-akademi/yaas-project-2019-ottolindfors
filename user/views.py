from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views import View

from user.forms import UserCreationFormWithEmail


class SignUp(View):
    def get(self, request):
        form = UserCreationFormWithEmail()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            new_user = form.save()  # Save the user with the save() function in UserCreationFormWithEmail
            messages.add_message(request, messages.INFO, "User created")
            user_info = "username " + new_user.username + ", email " + new_user.email
            messages.add_message(request, messages.INFO, user_info)
            # Sign in the user for ease of use
            auth.login(request, new_user)
            return redirect('index')  # Issue 001: does not give Http status code 302 (gives 200)
        else:
            messages.add_message(request, messages.INFO, "This username has been taken, or This email has been taken")  # Required by UC1
            return render(request, "signup.html", {"form": form})


class SignIn(View):

    def get(self, request):
        # Prevent phishing attacks. Check that redirect is safe if present un the url (?next=)
        destination = self.request.GET.get('next')
        destination_safe = is_safe_url(destination, allowed_hosts=None)

        # If no redirect
        if destination is None:
            destination_safe = True

        if destination_safe:
            return render(request, "signin.html")
        else:
            messages.add_message(
                request,
                messages.INFO,
                "Back to safety! The url you used contained a malicious attempt to redirect you to another site. "
                "Be careful of the urls you use when signing in. :)")
            return redirect("index")

    def post(self, request):
        username = request.POST.get('username', '')  # Empty '' tells the get method to return '' if username not found
        password = request.POST.get('password', '')  # Is this secure?

        user = auth.authenticate(username=username, password=password)

        if user is None:
            messages.add_message(request, messages.INFO, "Invalid username or password")
            return render(request, "signin.html")
        else:
            # Login the user and
            # Safely redirect the user according to ?next= in the url the form was get:ted with

            destination = self.request.GET.get('next')
            destination_safe = is_safe_url(destination, allowed_hosts=None)  # No external links are allowed (phishing)

            # Determine if safe to login (no external redirect attempt)
            if destination is None:
                # Log in the user
                auth.login(request, user)
                messages.add_message(request, messages.INFO, "Welcome! Signed in.")
                return redirect('index')
            elif destination is not None and destination_safe:
                # Log in the user
                auth.login(request, user)
                messages.add_message(request, messages.INFO, "Welcome! Signed in.")
                return redirect(destination)
            else:
                # Return to safety
                messages.add_message(
                    request,
                    messages.INFO,
                    "Back to safety! The url you used contained a malicious attempt to redirect you to another site. "
                    "Be careful of the urls you use when signing in. :)")
                return redirect("index")


@login_required
def signout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "Signed out.")
    return HttpResponseRedirect(reverse("index"))


class EditProfile(View):
    pass
