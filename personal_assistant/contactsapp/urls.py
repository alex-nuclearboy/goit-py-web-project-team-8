from django.urls import path
from . import views

app_name = "contactsapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("contacts/", views.my_contacts, name="contacts"),
    path("contacts/<int:contact_id>/", views.contact_details, name="contact_details"),
    path("add_contact/", views.ContactCreateView.as_view(), name="add_contact"),
    path("contact/<int:pk>/update", views.ContactUpdateView.as_view(), name="contact_update"),
    path("contact/<int:pk>/delete", views.ContactDeleteView.as_view(), name="contact_delete"),
    path("groups/", views.groups, name="groups"),
    path("group/<int:tag_id>/", views.group_details, name="group_details"),
    path("group/add/", views.GroupCreateView.as_view(), name="add_group"),
    path("group/<int:pk>/update", views.GroupUpdateView.as_view(), name="group_update"),
    path("group/<int:pk>/delete", views.GroupDeleteView.as_view(), name="group_delete"),
]
