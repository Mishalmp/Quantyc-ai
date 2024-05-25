# investment/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer,Transactions

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2']

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['product', 'investment_amount','withdraw_money']


