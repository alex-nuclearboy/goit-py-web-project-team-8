from django.urls import path
from . import views

app_name = "contactsapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("contacts/", views.my_contacts, name="contacts"),
    path("add_contact/", views.ContactCreateView.as_view(), name="add_contact"),
    path("contact/<int:pk>/update", views.ContactUpdateView.as_view(), name="contact_update"),
    path("contact/<int:pk>/delete", views.ContactDeleteView.as_view(), name="contact_delete"),
    path("register/", views.register, name="register"), 
    path("tags/", views.tags, name="tags"),
    path("tags/<int:tag_id>/", views.tag_details, name="tag_details"),
    path("add_tag/", views.TagCreateView.as_view(), name="add_tag"),
    path("tag/<int:pk>/update", views.TagUpdateView.as_view(), name="tag_update"),
    path("tag/<int:pk>/delete", views.TagDeleteView.as_view(), name="tag_delete"),
]