from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from yaas import settings


class CustomUser(AbstractUser):
    """custom CustomUser model that is used instead of django's built in User model. Email field is modified."""
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={'unique': "This email has been taken"}
    )


class UserLanguageModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    language = models.CharField(
        max_length=255,
        default="en"
    )
