from django import forms
from .models import Note, Tag


class TagForm(forms.ModelForm):
    name = forms.CharField(min_length=3, max_length=25, required=True, widget=forms.TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class NoteForm(forms.ModelForm):
    title = forms.CharField(min_length=5, max_length=255, required=True, widget=forms.TextInput())
    content = forms.CharField(min_length=5, max_length=255, required=False, widget=forms.Textarea(attrs={'rows': 4}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
