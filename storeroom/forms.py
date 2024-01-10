from django import forms
from .models import Product

class UpdateForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=('available','price')


class SearchForm(forms.Form):
    search=forms.CharField(max_length=255)

class CteateForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=('name','description','price','available')