from django import forms


class CustomForm(forms.Form):
    field_set_name = forms.CharField()

