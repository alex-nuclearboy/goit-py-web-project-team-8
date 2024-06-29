from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Note, Tag
from .forms import NoteForm, TagForm, NoteSearchForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .context_processors import get_language
from .translations import translations


@login_required
def note_list(request):
    """
    View function for displaying a list of notes associated with the logged-in user.

    Retrieves notes based on search queries and tag filters, handles pagination.

    Returns:
    HttpResponse: Rendered template with notes, tags, search form, and tag filter.
    """
    language = get_language(request)
    query = request.GET.get('q')
    tag_query = request.GET.get('tag')
    search_form = NoteSearchForm(request.GET, language=language)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')

    notes = Note.objects.filter(user=request.user)
    notes = notes.order_by('created_at')

    selected_tag_name = 'All'

    if query:
        notes = Note.objects.filter(
            Q(user=request.user) &
            (Q(title__icontains=query) | Q(content__icontains=query))
        ).distinct()
    elif tag_query and tag_query != 'All':
        notes = Note.objects.filter(tags__name__icontains=tag_query, user=request.user).distinct()
        selected_tag_name = tag_query

    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    try:
        notes = paginator.page(page_number)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    return render(request, 'notesapp/note_list.html', {
        'notes': notes,
        'tags': Tag.objects.filter(user=request.user),
        'search_form': search_form,
        "query": query,
        'selected_tag_name': selected_tag_name,
    })


@login_required
def note_details(request, id):
    """
    View function for displaying details of a specific note.

    Retrieves and displays the note based on the provided ID.

    Args:
    id (int): The ID of the note to display
    """


