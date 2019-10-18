import decimal

from django import forms
from django.db.models import Max


class CreateAuctionForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea())
    minimum_price = forms.DecimalField(decimal_places=2, max_digits=15, min_value=decimal.Decimal("0.01"))   # allow up to 1 000 000 000 000.00
    deadline_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M:%S'],
        widget=forms.TextInput(attrs={"placeholder": "dd.mm.yyyy HH:MM:SS"}),
        help_text="Give the date as dd.mm.yyyy HH:MM:SS",
        label="Deadline"
    )


class ConfirmForm:
    pass


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
