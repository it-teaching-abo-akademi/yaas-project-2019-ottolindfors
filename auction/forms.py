from django import forms


class CreateAuctionForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea())
    minimum_price = forms.FloatField(min_value=0.01)
    deadline_date = forms.DateTimeField(input_formats=['%d.%m.%Y %H:%M:%S'],
                                   widget=forms.TextInput(attrs={"placeholder": "dd.mm.yyyy HH:MM:SS"}),
                                   help_text="Give the date as dd.mm.yyyy HH:MM:SS",
                                   label="Deadline")
