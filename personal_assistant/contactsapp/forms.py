from django import forms
from django.core.exceptions import ValidationError

from .models import Contact, Group
from .localize import text_array as translations


class ContactForm(forms.ModelForm):

    name = forms.CharField(
        min_length=3,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": "true"})
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
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='------'  # This ensures that the group field can be empty
    )

    class Meta:
        model = Contact
        fields = ["name", "phone", "email", "address", "birthday", "group"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
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
        if self.user is not None:
            groups = Group.objects.filter(creator=self.user)
            translated_groups = []
            for group in groups:
                if group.name == 'Family':
                    group.name = self.trans['family_group']
                elif group.name == 'Friends':
                    group.name = self.trans['friends_group']
                elif group.name == 'Work':
                    group.name = self.trans['work_group']
                translated_groups.append(group)
            self.fields['group'].queryset = Group.objects.filter(creator=self.user)
            self.fields['group'].choices = [('', '------')] + [(group.id, group.name) for group in translated_groups]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if self.instance.pk:
            # Exclude the current instance from the check
            if Contact.objects.filter(creator=self.user, name=name).exclude(pk=self.instance.pk).exists():
                raise ValidationError(self.trans['duplicate_contact'])
        else:
            if Contact.objects.filter(creator=self.user, name=name).exists():
                raise ValidationError(self.trans['duplicate_contact'])

        return cleaned_data


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
        self.user = kwargs.pop('user', None)
        language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(language, translations['en'])
        self.fields['name'].label = self.trans['group_name']
        self.fields['name'].widget.attrs.update({'placeholder': self.trans['group_name_placeholder']})

        if self.user is not None:
            self.fields['name'].queryset = Group.objects.filter(creator=self.user)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if self.instance.pk:
            # Exclude the current instance from the check
            if Group.objects.filter(creator=self.user, name=name).exclude(pk=self.instance.pk).exists():
                raise ValidationError(self.trans['duplicate_group'])
        else:
            if Group.objects.filter(creator=self.user, name=name).exists():
                raise ValidationError(self.trans['duplicate_group'])

        return cleaned_data


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