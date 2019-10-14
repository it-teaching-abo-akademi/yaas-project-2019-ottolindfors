from django import forms
from django.db.models import Max




class CreateAuctionForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea())
    minimum_price = forms.FloatField(min_value=0.01)
    deadline_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M:%S'],
        widget=forms.TextInput(attrs={"placeholder": "dd.mm.yyyy HH:MM:SS"}),
        help_text="Give the date as dd.mm.yyyy HH:MM:SS",
        label="Deadline"
    )


# class BidForm(forms.Form):
#     new_price = forms.FloatField()

# class BidForm(forms.ModelForm):
#     class Meta:
#         model = BidModel
#         fields = ('new_price',)
#
#     def save(self, commit=True):
#         bid = super(BidForm, self).save(commit=False)
#
