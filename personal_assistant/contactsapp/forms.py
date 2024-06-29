from typing import Any

from django.forms import ModelForm

from .models import Contact


class ContactForm(ModelForm):
    
    class Contact:
        model = Contact
        fields = ["name", "phone", "email", "address", "birth_day", "birth_month", "birth_year", "tags"]
