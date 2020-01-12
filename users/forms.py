from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class UserFilterForm(forms.Form):
    from_date = forms.DateField(widget=DateInput)
    to_date = forms.DateField(widget=DateInput)
