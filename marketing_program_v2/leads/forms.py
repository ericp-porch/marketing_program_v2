from django import forms

########################
# DATA TYPES INCLUDE:
# string =
# boolean --> true/false
# currency -> float numbers
# date =
# datetime --> same as date
# email
# float =
# integer
# phone --> string
# text --> string
# url --> string
# String, integer, float, string, boolean


#######################

class FilterForm(forms.Form):
    name = forms.CharField()
