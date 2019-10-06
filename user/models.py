from django.db import models

'''
Django docs: https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model
If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model 
is sufficient for you. This model behaves identically to the default user model, but you’ll be able to customize it in 
the future if the need arises:


Warning

You cannot change the AUTH_USER_MODEL setting during the lifetime of a project (i.e. once you have made and migrated 
models that depend on it) without serious effort. It is intended to be set at the project start, and the model it refers
to must be available in the first migration of the app that it lives in. See Substituting a custom User model (above) 
for more details.
'''

