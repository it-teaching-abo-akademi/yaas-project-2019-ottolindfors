from django import forms
from django.forms import ModelForm

from .models import CustomUser


# The UserCreationForm is just a ModelForm so
# https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
class CustomUserCreationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Make input invisible in browser

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


class EditUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Make input invisible in browser

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        # exclude = ['username']


#class SignInForm