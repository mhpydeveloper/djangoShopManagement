from django import forms
from django.core.exceptions import ValidationError

class CartAddForm(forms.Form):
	quantity = forms.IntegerField(min_value=1,max_value=999)



class CustomerForm(forms.Form):
    customer=forms.CharField(max_length=255)