from django.urls import path
from . import views

app_name = 'notesapp'

urlpatterns = [
    path('notes/', views.note_list, name='note_list'),
    path('note/add/', views.add_note, name='add_note'),
    path('note/<int:id>/details/', views.note_details, name='note_details'),
    path('note/<int:id>/edit', views.edit_note, name='edit_note'),
    path('note/<int:id>/delete', views.delete_note, name='delete_note'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tag/add/', views.add_tag, name='add_tag'),
    path('tag/<int:id>/delete', views.delete_tag, name='delete_tag'),
]
