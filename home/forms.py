from django import forms
from home.models import Product

from django.forms.widgets import NumberInput

class ShoppingCartOrderForm(forms.Form):
    first_name = forms.CharField(label='', min_length=3, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(label='', min_length=3, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(label='', min_length=6, max_length=128, widget=forms.TextInput(attrs={'placeholder': 'email'}))
    phone_number = forms.CharField(label='', max_length=12, required=False, widget=forms.TextInput(attrs={'placeholder': 'nr tel'}))
    post_code = forms.CharField(label='', min_length=6, max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Kod pocztowy'}))
    adress = forms.CharField(label='', min_length=3, max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Ulica i nr domu'}))
    city = forms.CharField(label='', min_length=3, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Miasto'}))
    country = forms.CharField(label='', min_length=3, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Kraj'}))
    descryption = forms.CharField(label='', max_length=2000, required=False, widget=forms.Textarea(attrs={'cols':40,'rows':10, 'placeholder': 'Komentarz do zamówienia'}))

#class ShoppingCartAddForms(forms.Form):
#   id_product = forms.CharField()
    #product_quantity = forms.CharField(initial='1')