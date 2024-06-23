from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm
)
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import (
    validate_password,
    get_default_password_validators
)

from .models import Profile
from .translations import translations


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.language = kwargs.pop('language', 'en')
        self.trans = translations.get(self.language, translations['en'])
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': self.trans['enter_username'],
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': self.trans['enter_email'],
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': self.trans['enter_password'],
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': self.trans['confirm_password'],
            'class': 'form-control'
        })
        self.fields['username'].label = self.trans['username']
        self.fields['email'].label = self.trans['email']
        self.fields['password1'].label = self.trans['password']
        self.fields['password2'].label = self.trans['password_confirmation']

        self.error_messages.update({
            'password_mismatch': self.trans['password_mismatch'],
            'username_exists': self.trans['username_exists'],
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['username_exists'])
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch']
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        self._validate_custom_password()

    def _validate_custom_password(self):
        password = self.cleaned_data.get('password1')
        if password:
            errors = []
            try:
                validate_password(
                    password, self.instance,
                    password_validators=get_default_password_validators()
                )
            except forms.ValidationError as e:
                for message in e.messages:
                    if 'too short' in message:
                        errors.append(self.trans['password_too_short'])
                    elif 'too common' in message:
                        errors.append(self.trans['password_too_common'])
                    elif 'entirely numeric' in message:
                        errors.append(self.trans['password_entirely_numeric'])
                    else:
                        errors.append(message)
            if errors:
                self.add_error('password1', forms.ValidationError(errors))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.language = kwargs.pop('language', 'en')
        self.trans = translations.get(self.language, translations['en'])
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.trans['enter_username'],
            'autofocus': True
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': self.trans['enter_password'],
        })
        self.fields['username'].label = self.trans['username']
        self.fields['password'].label = self.trans['password']

    class Meta:
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.trans['username_or_password_didnt_match'],
                    code='invalid_login',
                )
            if not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.trans['inactive_account'],
                    code='inactive',
                )
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Profile
        fields = ['avatar']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(),
    )
