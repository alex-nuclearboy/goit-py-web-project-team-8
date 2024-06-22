from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from smtplib import SMTPException

from .forms import (
    RegisterForm,
    LoginForm,
    ProfileForm,
    CustomPasswordResetForm
)


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='newsapp:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='newsapp:index')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(
        request, 'users/signup.html', context={"form": RegisterForm()}
    )


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='newsapp:index')

    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='newsapp:index')

    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='newsapp:index')


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(
        request, 'users/profile.html', {'profile_form': profile_form}
    )


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
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
            except SMTPException as err:
                print(f"SMTP error occurred: {err}")
                messages.error(
                    self.request,
                    "An error occurred while sending the email. "
                    "Please try again later."
                )
                return redirect('users:password_reset')
        else:
            messages.error(
                self.request,
                'No account found with the specified email address.'
            )
            return redirect('users:password_reset')


def password_reset_request(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                return CustomPasswordResetView.as_view()(request)
            else:
                messages.error(
                    request,
                    'No account found with the specified email address.'
                )
                return redirect('users:password_reset')
    else:
        form = CustomPasswordResetForm()
    return render(request, "users/password_reset.html", {"form": form})
