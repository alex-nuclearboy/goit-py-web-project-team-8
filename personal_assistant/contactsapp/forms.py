from typing import Any

from django.forms import ModelForm, CharField, EmailField, PasswordInput

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Contact, Tag


class ContactForm(ModelForm):
    
    class Contact:
        model = Contact
        fields = ["name", "phone", "email", "address", "birth_day", "birth_month", "birth_year", "tags"]

class CustomUserCreationForm(UserCreationForm):  
    username = CharField(label='Username', min_length=5, max_length=150)  
    email = EmailField(label='Email')  
    password1 = CharField(label='Password', widget=PasswordInput)  
    password2 = CharField(label='Confirm password', widget=PasswordInput)
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user
        