from django.urls import path
from . import views

app_name = "contactsapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("contacts/", views.my_contacts, name="contacts"),
    path("contact/add", views.ContactCreateView.as_view(), name="add_contact"),
    path("contact/<int:contact_id>/", views.contact_details, name="contact_details"),
    path("contact/<int:pk>/update", views.ContactUpdateView.as_view(), name="update_contact"),
    path("contact/<int:pk>/delete", views.ContactDeleteView.as_view(), name="delete_contact"),
    path("groups/", views.groups, name="groups"),
    path("group/add/", views.GroupCreateView.as_view(), name="add_group"),
    path("group/<int:pk>/update", views.GroupUpdateView.as_view(), name="update_group"),
    path("group/<int:pk>/delete", views.delete_group, name="delete_group"),
]
