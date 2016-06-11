from django import forms


class CustomForm(forms.Form):
    name = forms.CharField()
