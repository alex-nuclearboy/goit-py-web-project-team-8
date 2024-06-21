from django.urls import path
from . import views

app_name = "newsapp"

urlpatterns = [
    path('home/', views.main, name='index'),
]
