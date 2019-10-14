from django import forms
from django.forms import ModelForm

from .models import CustomUser


# The UserCreationForm is just a ModelForm so
# https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
class CustomUserCreationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Make input invisible in browser

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomUserEditForm2(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)  # Make input invisible in browser
    email = forms.EmailField(required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class CustomUserEditForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)  # Make input invisible in browser


# class SignInForm
