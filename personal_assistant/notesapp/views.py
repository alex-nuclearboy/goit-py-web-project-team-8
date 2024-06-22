from django.shortcuts import render, get_object_or_404, redirect
from .models import Note, Tag
from .forms import NoteForm
from django.db.models import Q


def note_list(request):
    query = request.GET.get('q')
    tag_query = request.GET.get('tag')

    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    elif tag_query:
        notes = Note.objects.filter(tags__name__icontains=tag_query).distinct()
    else:
        notes = Note.objects.all()

    return render(request, 'notes/note_list.html', {'notes': notes, 'tags': Tag.objects.all()})


def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            form.save_m2m()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})


def edit_note(request, id):
    note = get_object_or_404(Note, id=id)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            form.save_m2m()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})


def delete_note(request, id):
    note = get_object_or_404(Note, id=id)
    if request.method == "POST":
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})

