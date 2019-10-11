

# Removed from user/forms.py
class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Email required")

    # Metadata (fields) from UserCreationForm
    class Meta:
        model = CustomUser    # the CustomUser model
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    # allows the form to save the data to the model
    # commit == 'save the data to the database'
    def save(self, commit=True):
        # super calls this extended class' save method in order to create a user (the save() calls create_user()).
        # but commit still False because we only want the user (object) and not save it to the database yet.
        # we still want to add email
        user = super(UserCreationFormWithEmail, self).save(commit=False)  # create user object

        # clean the email data
        user.email = self.cleaned_data["email"]

        # now save the user to the database, commit=True
        if commit:
            user.save()
        return user