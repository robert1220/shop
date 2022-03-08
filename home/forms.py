from django import forms

from django.forms.widgets import NumberInput

class ShoppingCartOrderForm(forms.Form):
    first_name = forms.CharField(label='Imię', min_length=1, max_length=64, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Nazwisko', min_length=1, max_length=64, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='e-mail', min_length=3, max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(label='Nr telefonu', max_length=12, required=False, widget=forms.TextInput(attrs={'placeholder': 'Pole nie obowiązkowe','class':'form-control'}))
    post_code = forms.CharField(label='Kod pocztowy', min_length=6, max_length=6, widget=forms.TextInput(attrs={'class':'form-control'}))
    adress = forms.CharField(label='Ulica', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(label='Miasto', max_length=64, widget=forms.TextInput(attrs={'class':'form-control'}))
    country = forms.CharField(label='Kraj', max_length=32, widget=forms.TextInput(attrs={'class':'form-control'}))
    descryption = forms.CharField(label='Komentarz do zamówienia', max_length=2000, required=False, widget=forms.Textarea(attrs={'rows':5, 'placeholder': 'Pole nie obowiązkowe','class':'form-control'}))
