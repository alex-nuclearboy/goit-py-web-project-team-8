from django.urls import path
from . import views

app_name = 'notesapp'

urlpatterns = [
    path('notes/', views.note_list, name='note_list'),
    path('add_note/', views.add_note, name='add_note'),
    path('tags/', views.tag_list, name='tag_list'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('note/<int:id>/edit', views.edit_note, name='edit_note'),
    path('note/<int:id>/delete', views.delete_note, name='delete_note'),
    path('tag/<int:id>/delete', views.delete_tag, name='delete_tag'),
]
