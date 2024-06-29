from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .localize import text_array

from django.contrib.auth.models import User
from .models import Contact, Group
from .forms import ContactForm, GroupForm
from .context_processors import get_language


@method_decorator(login_required, name='dispatch')
class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("contactsapp:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['language'] = get_language(self.request)
        return kwargs

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.creator = User.objects.get(id=self.request.user.id)
        fields.save()
        setattr(form.instance, self.author, self.request.user)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("contactsapp:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['language'] = get_language(self.request)
        return kwargs

    def get_queryset(self):
        return Contact.objects.filter(creator=self.request.user)


@method_decorator(login_required, name='dispatch')
class ContactDeleteView(DeleteView):
    model = Contact
    template_name_suffix = "_delete_form"
    success_url = reverse_lazy("contactsapp:index")

    def get_queryset(self):
        return Contact.objects.filter(creator=self.request.user)

##########################################################


@method_decorator(login_required, name='dispatch')
class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("contactsapp:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['language'] = get_language(self.request)
        return kwargs

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.creator = User.objects.get(id=self.request.user.id)
        fields.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("contactsapp:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['language'] = get_language(self.request)
        return kwargs

    def get_queryset(self):
        return Group.objects.filter(creator=self.request.user)


@method_decorator(login_required, name='dispatch')
class GroupDeleteView(DeleteView):
    model = Group
    template_name_suffix = "_delete_form"
    success_url = reverse_lazy("contactsapp:index")

    def get_queryset(self):
        return Group.objects.filter(creator=self.request.user)


def my_contacts(request):
    localization = text_array[get_language(request)]
    curr_user = request.user.id
    your_contacts = Contact.objects.filter(creator=curr_user).order_by("-creation_time")
    template = loader.get_template("contactsapp/contacts.html")
    context = {
        "contacts": your_contacts,
        "text": {
            "contact": localization['contact'],
            'list_empty': localization['contact_list_empty'],
            'list': localization['contact_list'],
            'group': localization['group'],
            'add': localization['add'],
            'add_cont': localization['add_cont'],
            'edit': localization['edit'],
            'delete': localization['delete']
        },
        "title": "Your contacts",
        "translations": localization,
    }
    return HttpResponse(template.render(context=context, request=request))


def contact_details(request, contact_id):
    localization = text_array[get_language(request)]
    contact = Contact.objects.get(pk=contact_id)
    template = loader.get_template("contactsapp/contact.html")
    creator = None
    if contact.creator == request.user:
        creator = True
    else:
        creator = False
    context = {
        "contact": contact,
        "text": {
            'group': localization['group'],
            'not_found': localization['contact_not_found'],
            'name': localization['contact_name'],
            'phone': localization['contact_phone'],
            'mail': localization['contact_mail'],
            'address': localization['contact_address'],
            'creation': localization['contact_creation'],
            'update': localization['contact_update'],
            'edit': localization['contact_edit'],
            'delete': localization['contact_delete']
        },
        "creator": creator,
        "title": contact.name,
        "translations": localization,
        }
    return HttpResponse(template.render(context=context, request=request))


def groups(request):
    localization = text_array[get_language(request)]
    groups = Group.objects.order_by("-id")
    template = loader.get_template("contactsapp/groups.html")
    context = {
        "groups": groups,
        "text": {
            'group': localization['group'],
            'list_empty': localization['group_list_empty'],
            'list': localization['group_list'],
            'groups': localization['groups'],
            'add_group': localization['add_group']
        },
        "title": "All groups",
        "translations": localization,
        }
    return HttpResponse(template.render(context=context, request=request))


def group_details(request, group_id):
    localization = text_array[get_language(request)]
    group = Group.objects.get(pk=group_id)
    contacts = Contact.objects.filter(group=group)
    template = loader.get_template("contactsapp/tag.html")
    creator = None
    if group.creator == request.user:
        creator = True
    else:
        creator = False
    context = {
        "group": group,
        "text": {
            "contacts_of_group": localization['contacts_of_group'],
            "groups": localization['groups'],
            'edit': localization['tag_edit'],
            'delete': localization['tag_delete']
        },
        "contacts": contacts,
        "creator": creator,
        "title": group.name,
        "translations": localization,
        }
    return HttpResponse(template.render(context=context, request=request))


def index(request):
    localization = text_array[get_language(request)]
    curr_user = request.user.id
    contacts = Contact.objects.filter(creator=curr_user).order_by("-creation_time")
    latest_contacts = contacts[:10]
    template = loader.get_template("contactsapp/index.html")
    context = {
        "text": {
            "contact": localization['contact'],
            'latest_empty': localization['contact_latest_empty'],
            'latest': localization['contact_latest'],
            'groups': localization['groups']
        },
        "translations": localization,
        "latest_contacts": latest_contacts,
        "contacts": contacts,
        "title": "Home page",
    }
    return HttpResponse(template.render(context=context, request=request))

