from django import forms
from .models import Note, Tag

class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']

