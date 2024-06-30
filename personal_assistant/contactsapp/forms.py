from django import forms

from .models import Contact, Group
from .localize import text_array as translations


class ContactForm(forms.ModelForm):

    name = forms.CharField(
        min_length=3,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": "true",})
    )
    phone = forms.CharField(
        min_length=9,
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    address = forms.CharField(
        min_length=10,
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        min_length=10,
        max_length=50,
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Contact
        fields = ["name", "phone", "email", "address", "birthday", "group"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(language, translations['en'])
        self.fields['name'].widget.attrs.update({'placeholder': self.trans['name_placeholder']})
        self.fields['name'].label = self.trans['name']
        self.fields['phone'].widget.attrs.update({'placeholder': self.trans['phone_placeholder']})
        self.fields['phone'].label = self.trans['phone']
        self.fields['address'].widget.attrs.update({'placeholder': self.trans['address_placeholder']})
        self.fields['address'].label = self.trans['address']
        self.fields['email'].widget.attrs.update({'placeholder': self.trans['email_placeholder']})
        self.fields['email'].label = self.trans['email']
        self.fields['birthday'].widget.attrs.update({'placeholder': self.trans['birthday_placeholder']})
        self.fields['birthday'].label = self.trans['birthday']
        self.fields['group'].label = self.trans['group']
        if user is not None:
            self.fields['group'].queryset = Group.objects.filter(creator=user)


class GroupForm(forms.ModelForm):
    name = forms.CharField(
        min_length=3,
        max_length=25,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": "true"})
    )

    class Meta:
        model = Group
        fields = ['name']

    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(language, translations['en'])
        self.fields['name'].label = self.trans['group_name']
        self.fields['name'].widget.attrs.update({'placeholder': self.trans['group_name_placeholder']})


class ContactSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
    )

    def __init__(self, *args, **kwargs):
        self.language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(self.language, translations['en'])
        self.fields['query'].widget.attrs.update({'placeholder': self.trans['search_field']})