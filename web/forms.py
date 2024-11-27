from django import forms
from .models import Contact
from ticket.models import Order

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        
        fields = ['name', 'email', 'subject', 'your_message']

    # Customize the widgets for specific fields
    widgets = {
        'name': forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Your Name'}),
        'email': forms.EmailInput(attrs={'class': 'custom-class', 'placeholder': 'Your Email'}),
        'subject': forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Subject'}),
        'your_message': forms.Textarea(attrs={'class': 'custom-class', 'placeholder': 'Your Message'}),
    }


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        widget=forms.TextInput(attrs={'type':'search','class': 'text-white js-search js-dd-focus', 'placeholder': 'Search Destinations'})
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'email', 'country']
        

