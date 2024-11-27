from django import forms
from ticket.models import Checkout


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['full_name', 'phone_number', 'email', 'confirm_email']    