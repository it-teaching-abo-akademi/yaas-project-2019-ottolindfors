from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

'''
Register the custom User model according to django docs: 
https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model
'''

admin.site.register(CustomUser, UserAdmin)
