from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .localize import text_array

from django.contrib.auth.models import User
from .models import Contact, Tag

#from .transfer import prepare_data_for_db

# Create your views here.
class ContactCreateView(CreateView):
    model = Contact
    author = "author"
    fields = ["name", "phone", "email", "address", "birth_day", "birth_month", "birth_year", "tags"]
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("contactsapp:index")
    
    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.creator = User.objects.get(id=self.request.user.id)
        fields.save()
        setattr(form.instance, self.author, self.request.user)
        return super().form_valid(form)


class ContactUpdateView(UpdateView):
    model = Contact
    fields = ["name", "phone", "email", "address", "birth_day", "birth_month", "birth_year", "tags"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("contactsapp:index")


class ContactDeleteView(DeleteView):
    model = Contact
    template_name_suffix = "_delete_form"
    success_url = reverse_lazy("contactsapp:index")
    
##########################################################

class TagCreateView(CreateView):
    model = Tag
    author = "author"
    fields = ["name"]
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("contactsapp:index")
    
    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.creator = User.objects.get(id=self.request.user.id)
        fields.save()
        setattr(form.instance, self.author, self.request.user)
        return super().form_valid(form)


class TagUpdateView(UpdateView):
    model = Tag
    fields = ["name"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("contactsapp:index")


class TagDeleteView(DeleteView):
    model = Tag
    template_name_suffix = "_delete_form"
    success_url = reverse_lazy("contactsapp:index")
    
def get_language(request):
    """
    Get the language from the request or session.
    - Retrieves the language from the GET parameters or session.
    - Defaults to English if no language is found.
    - Stores the language in the session.
    """
    language = request.GET.get('lang')
    if not language:
        language = request.session.get('language', 'en')
    request.session['language'] = language
    return language

# Create your views here.
def my_contacts(request):
    localization = text_array[get_language(request)]
    curr_user = request.user.id
    your_contacts = Contact.objects.filter(creator=curr_user).order_by("-creation_date")
    template = loader.get_template("contactsapp/contacts.html")
    context = {
        "contacts": your_contacts,
        "text":{
            "contact":localization['contact'],
            'list_empty':localization['list_empty'],
            'list':localization['list'],
            'tags':localization['tags'],
            'add':localization['add'],
            'edit':localization['edit'],
            'delete':localization['delete']
        },
        "title":"Your contacts"
    }
    return HttpResponse(template.render(context=context, request=request))

def contact_details(request, contact_id):
    contact = Contact.objects.get(pk=contact_id)
    template = loader.get_template("contactsapp/contact.html")
    creator = None
    if contact.creator == request.user:
        creator = True
    else:
        creator = False
    context = {
        "contact":contact,
        "creator":creator,
        "title":contact.name
        }
    return HttpResponse(template.render(context=context, request=request))

def tags(request):
    tags = Tag.objects.order_by("-name")
    template = loader.get_template("contactsapp/tags.html")
    context = {
        "tags":tags,
        "title":"All tags"
        }
    return HttpResponse(template.render(context=context, request=request))

def tag_details(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    contacts = Contact.objects.filter(tags=tag)
    template = loader.get_template("contactsapp/tag.html")
    creator = None
    if tag.creator == request.user:
        creator = True
    else:
        creator = False
    context = {
        "tag":tag,
        "contacts":contacts,
        "creator":creator,
        "title":tag.name
        }
    return HttpResponse(template.render(context=context, request=request))

def index(request):
    localization = text_array[get_language(request)]
    curr_user = request.user.id
    contacts = Contact.objects.filter(creator=curr_user).order_by("-creation_date")
    latest_contacts = contacts[:10]
    template = loader.get_template("contactsapp/index.html")
    context = {
        "text":{
            "contact":localization['contact'],
            'latest_empty':localization['latest_empty'],
            'latest':localization['latest'],
            'tags':localization['tags']
        },
        "latest_contacts": latest_contacts,
        "contacts": contacts,
        "title":"Home page"
    }
    return HttpResponse(template.render(context=context, request=request))
