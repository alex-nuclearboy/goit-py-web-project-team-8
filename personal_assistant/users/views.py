import os
import xml.etree.ElementTree as ET
from smtplib import SMTPException
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin

from .forms import (
    RegisterForm,
    LoginForm,
    ProfileForm,
    CustomPasswordResetForm
)


def load_translations(language):
    translations = {}
    file_path = os.path.join(
        os.path.dirname(__file__), 'locale', f'localisation_{language}.xml'
    )
    tree = ET.parse(file_path)
    root = tree.getroot()
    for item in root.findall('.//users/*'):
        key = item.tag
        value = item.get('text')
        translations[key] = value
    return translations


def signupuser(request):
    language = request.GET.get('lang')
    if language:
        request.session['language'] = language
    else:
        language = request.session.get('language', 'en')

    translations = load_translations(language)

    if request.user.is_authenticated:
        return redirect(to='newsapp:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='newsapp:index')
        else:
            return render(
                request, 'users/signup.html',
                context={"form": form, "translations": translations}
            )

    return render(
        request, 'users/signup.html',
        context={"form": RegisterForm(), "translations": translations}
    )


def loginuser(request):
    language = request.GET.get('lang')
    if language:
        request.session['language'] = language
    else:
        language = request.session.get('language', 'en')

    translations = load_translations(language)

    if request.user.is_authenticated:
        return redirect(to='newsapp:index')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is None:
                messages.error(
                    request, translations['username_or_password_didnt_match']
                )
                return render(
                    request, 'users/login.html',
                    context={"form": form, "translations": translations}
                )

            login(request, user)
            return redirect(to='newsapp:index')
    else:
        form = LoginForm()

    return render(
        request, 'users/login.html',
        context={"form": form, "translations": translations}
    )


@login_required
def logoutuser(request):
    language = request.GET.get('lang')
    if language:
        request.session['language'] = language
    else:
        language = request.session.get('language', 'en')

    translations = load_translations(language)

    logout(request)
    messages.success(request, translations['logout_success'])
    return redirect(to='newsapp:index')


@login_required
def profile(request):
    language = request.GET.get('lang')
    if language:
        request.session['language'] = language
    else:
        language = request.session.get('language', 'en')

    translations = load_translations(language)

    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, translations['profile_update_success'])
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(
        request, 'users/profile.html',
        {'profile_form': profile_form, "translations": translations}
    )


class TranslationsContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = self.request.GET.get('lang')
        if language:
            self.request.session['language'] = language
        else:
            language = self.request.session.get('language', 'en')
        context['translations'] = load_translations(language)
        return context


class CustomPasswordResetView(
    SuccessMessageMixin, TranslationsContextMixin, PasswordResetView
):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = ("An email with instructions to reset your password "
                       "has been sent to %(email)s.")
    subject_template_name = 'users/password_reset_subject.txt'
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            try:
                return super().form_valid(form)
            except SMTPException:
                messages.error(
                    self.request,
                    (
                        self.request.session.get('translations')
                        ['email_send_error']
                    )
                )
                return render(self.request, self.template_name, {
                    'form': form,
                    'translations': self.request.session.get('translations')
                })
        else:
            messages.error(
                self.request,
                (
                    self.request.session.get('translations')
                    ['password_reset_no_account']
                )
            )
            return render(self.request, self.template_name, {
                'form': form,
                'translations': self.request.session.get('translations')
            })


class CustomPasswordResetConfirmView(
    SuccessMessageMixin, TranslationsContextMixin, PasswordResetConfirmView
):
    template_name = 'users/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(
    SuccessMessageMixin, TranslationsContextMixin, PasswordResetCompleteView
):
    template_name = 'users/password_reset_complete.html'


class CustomPasswordResetDoneView(
    SuccessMessageMixin, TranslationsContextMixin, PasswordResetDoneView
):
    template_name = 'users/password_reset_done.html'


def password_reset_request(request):
    language = request.GET.get('lang')
    if language:
        request.session['language'] = language
    else:
        language = request.session.get('language', 'en')

    translations = load_translations(language)

    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                try:
                    return CustomPasswordResetView.as_view()(request)
                except SMTPException as err:
                    print(f"SMTP error occurred: {err}")
                    messages.error(
                        request,
                        translations['smtp_error']
                    )
                    return redirect('users:password_reset')
            else:
                messages.error(
                    request,
                    translations['password_reset_no_account']
                )
                return redirect('users:password_reset')
    else:
        form = CustomPasswordResetForm()

    return render(
        request, "users/password_reset.html",
        {"form": form, "translations": translations}
    )
