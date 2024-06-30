from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .localize import text_array

from django.contrib.auth.models import User
from .models import Contact, Group
from .forms import ContactForm, GroupForm, ContactSearchForm
from .context_processors import get_language


@method_decorator(login_required, name='dispatch')
class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contactsapp/contact_form.html"
    success_url = reverse_lazy("contactsapp:contacts")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['language'] = get_language(self.request)
        return kwargs

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.creator = self.request.user  # Set the creator field
        fields.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contactsapp/contact_form.html"
    success_url = reverse_lazy("contactsapp:contacts")

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
    template_name = "contactsapp/group_form.html"
    success_url = reverse_lazy("contactsapp:groups")

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
    template_name = "contactsapp/group_form.html"
    success_url = reverse_lazy("contactsapp:groups")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['language'] = get_language(self.request)
        return kwargs

    def get_queryset(self):
        return Group.objects.filter(creator=self.request.user)


@method_decorator(login_required, name='dispatch')
class GroupDeleteView(DeleteView):
    model = Group
    template_name_suffix = "_delete_form"
    success_url = reverse_lazy("contactsapp:groups")

    def get_queryset(self):
        return Group.objects.filter(creator=self.request.user)


@login_required
def my_contacts(request):
    language = get_language(request)
    localization = text_array[language]
    curr_user = request.user.id

    query = request.GET.get('query', '')
    group_id = request.GET.get('group_id')

    # Create the search form with the current query
    search_form = ContactSearchForm(request.GET, language=language)

    # Filter contacts based on query and group_id
    contacts = Contact.objects.filter(creator=curr_user)
    if group_id:
        contacts = contacts.filter(group_id=group_id)
    if query:
        contacts = contacts.filter(Q(name__icontains=query) | Q(phone__icontains=query))

    contacts = contacts.order_by("-creation_time")
    groups = Group.objects.filter(creator=curr_user)

    template = loader.get_template("contactsapp/contact_list.html")
    context = {
        "contacts": contacts,
        "groups": groups,
        "search_form": search_form,
        "text": {
            "contact": localization['contact'],
            'list_empty': localization['contact_list_empty'],
            'list': localization['contact_list'],
            'group': localization['group'],
            'add': localization['add'],
            'add_cont': localization['add_cont'],
            'edit': localization['edit'],
            'delete': localization['delete'],
            'create_group': localization['create_group'],
            'create_button': localization['create_button'],
            'update_group': localization['update_group'],
            'add_contact': localization['add_contact'],
            'go_to_groups': localization['go_to_groups'],
            'all': localization['all'],
            'search_field': localization['search_field'],
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
            'creation': localization['create_contact'],
            'update': localization['update_contact'],
            'edit': localization['contact_edit'],
            'delete': localization['contact_delete']
        },
        "creator": creator,
        "title": contact.name,
        "translations": localization,
        }
    return HttpResponse(template.render(context=context, request=request))


def groups(request):
    language = get_language(request)
    localization = text_array[language]
    user_groups = Group.objects.filter(creator=request.user).order_by("-id")
    for group in user_groups:
        group.display_name = group.name

    template = loader.get_template("contactsapp/group_list.html")
    context = {
        "groups": user_groups,
        "text": {
            'list': localization['group_list'],
            'list_empty': localization['group_list_empty'],
            'groups': localization['groups'],
            'add_group': localization['add_group'],
            'edit': localization['edit'],
            'delete': localization['delete'],
            'confirm_delete': localization['confirm_delete_group'],
            'back_to_contacts': localization['back_to_contacts']
        },
        "title": localization['all_groups'],
        "language": language,
        "translations": localization,
    }
    return HttpResponse(template.render(context=context, request=request))


@login_required
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk, creator=request.user)
    if request.method == 'POST':
        group.delete()
        return redirect('contactsapp:groups')
    return redirect('contactsapp:groups')


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
