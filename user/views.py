from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import View

from user.forms import CustomUserCreationForm, CustomUserEditForm
from user.models import CustomUser


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
        print('SignIn post safe_destination: ' + str(safe_destination))

        # TODO: Check with Postman that this is working (it is not working)
        if safe_destination:
            username = request.POST.get('username', '')  # Empty '' tells the get method to return '' if username not found
            password = request.POST.get('password', '')  # Is this secure?
            email = request.POST.get('email', '')

            print('username: .' + username + '.')
            print('password: .' + password + '.')
            print('email: .' + email + '.')

            # TODO: Figure out why testTDD always get user=None although username and password are correct
            user = auth.authenticate(username=username, password=password)

            print('Signin SIGNED IN: ' + str(user))

            print('user : .' + str(user) + '.')
            if user is None:
                # Invalid username or password
                messages.add_message(request, messages.INFO, "Invalid username or password")
                print("user is None")
                return render(request, "signin.html")
            else:
                # Log in the user
                auth.login(request, user)

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
    print('destination: ' + str(destination))

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
            form = CustomUserEditForm(instance=request.user)
            return render(request, "editprofile.html", {"form": form})
        else:
            messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
            return redirect("index")

    def post(self, request):
        safe_destination = safeRedirectDestination(request)
        if safe_destination:
            new_email = request.POST.get('email', '').strip()
            new_password = request.POST.get('password', '').strip()
            print('old email: ' + request.user.email)
            print('new email: ' + new_email)
            print('new password: ' + new_password)
            save = False
            user_in_db = CustomUser.objects.get(username=request.user.username)
            if new_email != '':
                # Check if email is taken
                email_available = False
                if CustomUser.objects.filter(email=new_email).count() == 0:
                    email_available = True
                else:
                    users = CustomUser.objects.filter(email=new_email).values_list('username', flat=True)
                    if len(users) == 1 and users[0] == request.user.username:
                        email_available = True
                if email_available:
                    print('email avalible')
                    user_in_db.email = new_email
                    save = True
                    messages.add_message(request, messages.INFO, "new email")
                else:
                    messages.add_message(request, messages.INFO, "email taken")
                    # return HttpResponseRedirect(reverse('user:editprofile'))
                    return redirect('user:editprofile')  # no status code 200 since not using a django form
            if new_password != '':
                user_in_db.set_password(new_password)
                save = True
                messages.add_message(request, messages.INFO, "new password")
            if save:
                user_in_db.save()
                update_session_auth_hash(request, user_in_db)  # Sign out (invalidate) all sessions
                auth.login(request, user_in_db)  # Sign in user in case password has changed (to pass testTDD)
                messages.add_message(request, messages.INFO, "User info saved")
                return redirect('index')
            else:
                messages.add_message(request, messages.INFO, "User info not saved")
                return redirect('index')
        else:
            messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
            return redirect("index")

        # TODO: Figure outh why hte form will not validate
        # if safe_destination:
        #     new_email = request.POST.get('email', '').strip()
        #     new_password = request.POST.get('password', '').strip()
        #     print('.' + new_email + '.', '.' + new_password + '.')
        #     user_in_db = CustomUser.objects.filter(username=request.user.username)
        #     update = False
        #     if new_email != '' and new_password != '':
        #         print('#')
        #         form = CustomUserEditForm({'email': new_email, 'password': new_password}, instance=user_in_db)
        #         update = True
        #     elif new_email != '' and new_password == '':
        #         print('##')
        #         form = CustomUserEditForm({'email': new_email}, instance=user_in_db)
        #         update = True
        #     elif new_email == '' and new_password != '':
        #         print('## #')
        #         form = CustomUserEditForm({'password': new_password}, instance=user_in_db)
        #         update = True
        #
        #     if update:
        #         print('## ##')
        #         if form.is_valid():
        #             print('## ## #')
        #             form.save()
        #             messages.add_message(request, messages.INFO, "Profile updated")
        #             return redirect('index')
        #     else:
        #         print('## ## ##')
        #         messages.add_message(request, messages.INFO, "Nothing updated")
        #         return redirect('index')
        # else:
        #     messages.add_message(request, messages.INFO, "Back to safety! Malicious attempt to redirect.")
        #     return redirect("index")
