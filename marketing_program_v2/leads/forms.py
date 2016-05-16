from django import forms

########################
# DATA TYPES INCLUDE:
# string = string
# boolean = true/false
# currency = float numbers
# date = date
# datetime = date
# email = string
# float = float
# integer = integer
# phone = string
# text = string
# url = string
# String, integer, float, string, boolean


#######################

class FilterForm(forms.Form):
    name = forms.CharField()
