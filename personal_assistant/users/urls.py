from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('signup/', views.signupuser, name='signup'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path(
        'reset-password/',
        views.password_reset_request,
        name='password_reset'
    ),
    path(
        'reset-password/done/',
        views.CustomPasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset-password/confirm/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url='/users/reset-password/complete/'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset-password/complete/',
        views.CustomPasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
