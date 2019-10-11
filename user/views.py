from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views import View

from user.forms import CustomUserCreationForm


class SignUp(View):

    def get(self, request):
        safe_deastination = safeRedirectDestination(request)
        if safe_deastination:
            form = CustomUserCreationForm()
            return render(request, "signup.html", {"form": form})
        else:
            messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
            return redirect("index")

    def post(self, request):
        safe_destination = safeRedirectDestination(request)

        # TODO: Check with Postman that this is working
        if safe_destination:
            form = CustomUserCreationForm(request.POST)

            if form.is_valid():
                # Save the user with the save() function in CustomUserCreationForm
                new_user = form.save()

                # Messages
                messages.add_message(request, messages.INFO, "User created")
                user_info = "username " + new_user.username + ", email " + new_user.email
                messages.add_message(request, messages.INFO, user_info)

                # Sign in the user for ease of use
                auth.login(request, new_user)

                return redirect('index')  # Issue 001
            else:
                messages.add_message(request, messages.INFO, "This username has been taken, or This email has been taken")  # Required by UC1
                return render(request, "signup.html", {"form": form})
        else:
            messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
            return redirect("index")


class SignIn(View):

    def get(self, request):
        safe_destination = safeRedirectDestination(request)

        if safe_destination:
            return render(request, "signin.html")
        else:
            messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
            return redirect("index")

    def post(self, request):
        safe_destination = safeRedirectDestination(request)

        # TODO: Check with Postman that this is working
        if safe_destination:
            username = request.POST.get('username', '')  # Empty '' tells the get method to return '' if username not found
            password = request.POST.get('password', '')  # Is this secure?

            user = auth.authenticate(username=username, password=password)

            if user is None:
                # Invalid username or password
                messages.add_message(request, messages.INFO, "Invalid username or password")
                return render(request, "signin.html")
            else:
                # Log in the user
                auth.login(request, user)

                messages.add_message(request, messages.INFO, "Welcome! Signed in.")
                print("SIGNED IN")

                destination = request.GET.get('next')
                if destination is None:
                    return redirect('index')
                else:
                    return redirect(destination)
        else:
            # Return to safety
            messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
            return redirect("index")


def safeRedirectDestination(request):
    # Prevent phishing attacks. Check that redirect is safe if present un the url (?next=)
    destination = request.GET.get('next')
    destination_safe = is_safe_url(destination, allowed_hosts=None)

    # If no redirect
    if destination is None:
        destination_safe = True  # prevent destination_safe == False

    if destination_safe:
        return True
    else:
        return False


@login_required
def signout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "Signed out.")
    return HttpResponseRedirect(reverse("index"))


class EditProfile(View):
    pass
