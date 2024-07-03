from django.urls import path
from .views import upload_file, file_list, manage_category, download_file, delete_file

app_name = "filemanagerapp"

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('files/<str:category>/', file_list, name='file_list_by_category'),
    path('files/', file_list, name='file_list'),
    path('categories/manage/', manage_category, name='manage_category'),
    path('files/download/<int:file_id>/', download_file, name='download_file'),
    path('files/delete/<int:file_id>/', delete_file, name='delete_file'),
]