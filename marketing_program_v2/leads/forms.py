from django import forms

########################
# DATA TYPES INCLUDE:
# string
# boolean
# currency
# date
# datetime
# email
# float
# integer
# phone
# text
# url
#######################

class FilterForm(forms.Form):
    name = forms.CharField()
