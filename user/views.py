from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import translation
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import View

from user.forms import CustomUserCreationForm, CustomUserEditForm
from user.models import CustomUser, UserLanguageModel


class SignUp(View):

    def get(self, request):
        safe_destination = safeRedirectDestination(request)
        if safe_destination:
            form = CustomUserCreationForm()
            return render(request, "signup.html", {"form": form})
        else:
            messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
            return redirect("index")

    def post(self, request):
        safe_destination = safeRedirectDestination(request)

        if safe_destination:
            form = CustomUserCreationForm(request.POST)

            if form.is_valid():
                # Save the user with the save() function in CustomUserCreationForm
                new_user = form.save()

                # Set language
                try:
                    language = request.session[translation.LANGUAGE_SESSION_KEY]
                except KeyError:
                    language = 'en'
                user_language = UserLanguageModel(user=new_user, language=language)
                user_language.save()

                # Messages
                messages.add_message(request, messages.INFO, "User created")
                user_info = "username " + new_user.username + ", email " + new_user.email + ", language " + user_language.language
                messages.add_message(request, messages.INFO, user_info)

                # Sign in the user for ease of use
                auth.login(request, new_user)
                print('Signup SIGNED IN: ' + str(new_user.is_authenticated))

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

        if safe_destination:
            username = request.POST.get('username', '')  # Empty '' tells the get method to return '' if username not found
            password = request.POST.get('password', '')  # Is this secure?

            user = auth.authenticate(username=username, password=password)

            if user is None:
                # Invalid username or password
                messages.add_message(request, messages.INFO, "Invalid username or password")
                print("user is None")
                return render(request, "signin.html")
            else:
                # Log in the user
                auth.login(request, user)

                # Change language
                lang_code = UserLanguageModel.objects.get(user=user).language
                translation.activate(lang_code)
                request.session[translation.LANGUAGE_SESSION_KEY] = lang_code

                messages.add_message(request, messages.INFO, "Welcome! Signed in.")
                print("SIGNED IN: " + username)

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


@method_decorator(login_required, name='dispatch')
class EditProfile(View):
    def get(self, request):
        safe_destination = safeRedirectDestination(request)
        if safe_destination:
            # form = CustomUserEditForm(instance=request.user)
            initial_data = {'email': request.user.email, 'password': ''}
            form = CustomUserEditForm(initial=initial_data)
            return render(request, "editprofile.html", {"form": form})
        else:
            messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
            return redirect("index")

    def post(self, request):
        safe_destination = safeRedirectDestination(request)
        if safe_destination:
            form = CustomUserEditForm(request.POST)
            if form.is_valid():
                cdata = form.cleaned_data
                new_email = cdata['email']
                new_password = cdata['password']
                print('new email: ' + new_email)
                print('new password: ' + new_password)
                save = False
                user_in_db = CustomUser.objects.get(username=request.user.username)
                if new_email != '':
                    # Check if email is taken
                    email_available = False
                    if not CustomUser.objects.filter(email=new_email).exists():
                        email_available = True
                    else:
                        email_owner = CustomUser.objects.get(email=new_email).username  # works because email is unique
                        # Check if email belong to the current user (request.user)
                        if email_owner == user_in_db.username:
                            email_available = True
                        # users = CustomUser.objects.filter(email=new_email).values_list('username', flat=True)
                        # if len(users) == 1 and users[0] == request.user.username:
                        #     email_available = True
                    if email_available:
                        print('email avalible')
                        user_in_db.email = new_email
                        save = True
                        messages.add_message(request, messages.INFO, "new email")
                    else:
                        messages.add_message(request, messages.INFO, "email taken")
                        return render(request, "editprofile.html", {"form": form})  # no status code 200 since not using a django form
                if new_password != '':
                    # Set new password
                    user_in_db.set_password(new_password)
                    save = True
                    messages.add_message(request, messages.INFO, "new password")
                if save:
                    # Save the updated information
                    user_in_db.save()
                    update_session_auth_hash(request, user_in_db)  # Sign out (invalidate) all sessions
                    auth.login(request, user_in_db)  # Sign in user in case password has changed (to pass testTDD)
                    messages.add_message(request, messages.INFO, "User info updated")
                    return redirect('index')
                else:
                    messages.add_message(request, messages.INFO, "User info not updated")
                    return redirect('index')
            else:
                messages.add_message(request, messages.INFO, "Form invalid")
                return render(request, "editprofile.html", {"form": form})
        else:
            messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
            return redirect("index")
