from django import forms
from .models import Note, Tag
from django.core.exceptions import ValidationError


class TagForm(forms.ModelForm):
    name = forms.CharField(min_length=3, max_length=25, required=True, widget=forms.TextInput())

    class Meta:
        model = Tag
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(user=self.user, name=name).exists():
            raise ValidationError('A tag with this name already exists.')
        return name


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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if self.instance.pk:  # If the form edits an existing note
            if Note.objects.filter(user=self.user, title=title).exclude(pk=self.instance.pk).exists():
                raise ValidationError('A note with this title already exists.')
        else:  # If this is a new note
            if Note.objects.filter(user=self.user, title=title).exists():
                raise ValidationError('A note with this title already exists.')
        return title


class NoteSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        max_length=100,
        label='',
        widget=forms.TextInput()
    )
