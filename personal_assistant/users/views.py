from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import (
    RegisterForm,
    LoginForm,
    ProfileForm
)
from .translations import translations


def get_language(request):
    """
    Get the language from the request or session.
    If not found, default to English.
    """
    language = request.GET.get('lang')
    if not language:
        language = request.session.get('language', 'en')
    request.session['language'] = language
    return language


def signupuser(request):
    """
    Handle user registration.
    - If the user is already authenticated, redirect to the home page.
    - If the request method is POST, validate and save the form data.
    - If the form is valid, save the user and redirect to the home page.
    - If the form is invalid, re-render the registration page with errors.
    """
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    if request.user.is_authenticated:
        return redirect(to='newsapp:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST, language=language)
        if form.is_valid():
            form.save()
            return redirect(to='newsapp:index')
        else:
            return render(
                request, 'users/signup.html',
                context={"form": form, "translations": trans}
            )

    form = RegisterForm(language=language)
    return render(
        request, 'users/signup.html',
        context={"form": form, "translations": trans}
    )


def loginuser(request):
    """
    Handle user login.
    - If the user is already authenticated, redirect to the home page.
    - If the request method is POST, validate the login form.
    - If the form is valid, authenticate and log in the user.
    - If authentication fails, display an error message.
    - If the form is invalid, display form errors.
    """
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    if request.user.is_authenticated:
        return redirect(to='newsapp:index')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST, language=language)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, trans['login_success'])
                return redirect(to='newsapp:index')
            else:
                messages.error(
                    request, trans['username_or_password_didnt_match']
                )
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = LoginForm(language=language)

    return render(
        request, 'users/login.html',
        context={"form": form, "translations": trans}
    )


@login_required
def logoutuser(request):
    """
    Handle user logout.
    - Log out the user and redirect to the home page.
    - Display a success message upon logout.
    """
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    logout(request)
    messages.success(request, trans['logout_success'])
    request.session['language'] = language  # Save language after exiting
    return redirect(to='newsapp:index')


@login_required
def profile(request):
    """
    Handle user profile.
    - Display and update the user's profile information.
    - If the request method is POST, validate and save the profile form.
    - If the form is valid, save the profile and display a success message.
    - If the form is invalid, re-render the profile page with errors.
    """
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, trans['profile_update_success'])
            return redirect('users:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(
        request, 'users/profile.html',
        context={'profile_form': profile_form, 'translations': trans}
    )
