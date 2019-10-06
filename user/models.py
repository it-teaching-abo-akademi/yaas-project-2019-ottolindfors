from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

'''
1.
Django docs: https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model
If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model 
is sufficient for you. This model behaves identically to the default user model, but you’ll be able to customize it in 
the future if the need arises:


Warning

You cannot change the AUTH_USER_MODEL setting during the lifetime of a project (i.e. once you have made and migrated 
models that depend on it) without serious effort. It is intended to be set at the project start, and the model it refers
to must be available in the first migration of the app that it lives in. See Substituting a custom User model (above) 
for more details.


2.
In class CustomUser(AbstractUser):
For the email arguments see: https://github.com/django/django/blob/master/django/contrib/auth/models.py#L316
and https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username#Create%20a%20custom%20User%20model"""


3.
Referencing the User model (e.g. FOREIGN KEY) should be done with django.contrib.auth.get_user_model()
https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#referencing-the-user-model
    
    
4. 
Migration files are stored in:
External Libraries 
> Python 3.6 (yaas-...) 
> site-packages
> django
> contrib
> auth
> migrations
'''


class CustomUser(AbstractUser):
    """custom CustomUser model that is used instead of django's built in User model. Email field is modified."""
    pass
    # email = models.EmailField(
    #     _('email address'),
    #     unique=True,
    #     error_messages={'unique': _("This email has been taken")}
    # )
