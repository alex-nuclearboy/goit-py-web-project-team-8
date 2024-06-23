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
        views.CustomPasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset-password/confirm/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset-password/complete/',
        views.CustomPasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]
