from django.urls import path
from . import views

app_name = 'filemanagerapp'

urlpatterns = [
    path(
        'category/manage/',
        views.category_management,
        name='category_management'
    ),
    path(
        'category/add/',
        views.create_category,
        name='create_category'
    ),
    path(
        'category/<int:category_id>/delete/',
        views.delete_category,
        name='delete_category'
    ),
    path(
        'category/file/<int:file_id>/edit/',
        views.edit_file_category,
        name='edit_file_category'
    ),

    path('files/', views.file_list, name='file_list'),
    path('file/upload/', views.file_upload, name='file_upload'),
    path(
        'file/<int:file_id>/download/',
        views.file_download,
        name='file_download'
    ),
    path(
        'file/<int:file_id>/delete/',
        views.file_delete,
        name='file_delete'
    ),
]
