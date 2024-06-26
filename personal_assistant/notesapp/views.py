from django.shortcuts import render, get_object_or_404, redirect
from .models import Note, Tag
from .forms import NoteForm, TagForm, NoteSearchForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def note_list(request):
    query = request.GET.get('q')
    tag_query = request.GET.get('tag')
    search_form = NoteSearchForm(request.GET)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')

    notes = Note.objects.filter(user=request.user)  # Ensure we only get notes for the logged-in user

    selected_tag_name = 'All'

    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    elif tag_query and tag_query != 'All':
        notes = Note.objects.filter(tags__name__icontains=tag_query).distinct()
        selected_tag_name = tag_query

    # Setting up pagination
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


def note_details(request, id):
    note = get_object_or_404(Note, pk=id, user=request.user)
    return render(request, 'notesapp/note_details.html', {"note": note})


def tag_list(request):
    tags = Tag.objects.filter(user=request.user)

    # Setting up pagination
    paginator = Paginator(tags, 10)
    page_number = request.GET.get('page')
    try:
        tags = paginator.page(page_number)
    except PageNotAnInteger:
        tags = paginator.page(1)
    except EmptyPage:
        tags = paginator.page(paginator.num_pages)

    return render(request, 'notesapp/tag_list.html', {'tags': tags, 'tag_form': TagForm()})


def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            form.save_m2m()

            # Handling tags
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags.iterator():
                note.tags.add(tag)

            return redirect('notesapp:note_list')
        else:
            tags = Tag.objects.filter(user=request.user).all()
            return render(request, 'notesapp/note_form.html', {"tags": tags, 'form': form})
    else:
        return render(request, 'notesapp/note_form.html', {'form': NoteForm(user=request.user)})


def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST, user=request.user)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='notesapp:tag_list')
        else:
            tags = Tag.objects.filter(user=request.user)
            return render(request, 'notesapp/tag_list.html', {'tags': tags, 'tag_form': form})

    return redirect('notesapp:tag_list')


def edit_note(request, id):
    note = get_object_or_404(Note, id=id)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            note = form.save()

            # Handling tags
            selected_tags = request.POST.getlist('tags')
            choice_tags = Tag.objects.filter(
                name__in=selected_tags, user=request.user
            )
            for tag in choice_tags:
                note.tags.add(tag)

            return redirect('notesapp:note_list')
    else:
        form = NoteForm(instance=note, user=request.user)
    return render(request, 'notesapp/note_form.html', {'form': form})


def delete_note(request, id):
    note = get_object_or_404(Note, id=id,  user=request.user)
    if request.method == "POST":
        note.delete()
        return redirect('notesapp:note_list')
    return redirect('notesapp:note_list')


def delete_tag(request, id):
    tag = get_object_or_404(Tag, id=id, user=request.user)
    if request.method == 'POST':
        tag.delete()
        return redirect('notesapp:tag_list')
    return redirect('notesapp:tag_list')
