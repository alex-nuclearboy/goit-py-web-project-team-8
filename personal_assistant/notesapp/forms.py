from django import forms
from .models import Note, Tag
from django.core.exceptions import ValidationError
from .translations import translations


class TagForm(forms.ModelForm):
    name = forms.CharField(min_length=3, max_length=25, required=True, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    class Meta:
        model = Tag
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(self.language, translations['en'])
        self.fields['name'].widget.attrs.update({'placeholder': self.trans['enter_tag_name']})
        self.fields['name'].label = self.trans['tag_name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(user=self.user, name=name).exists():
            raise ValidationError(self.trans['tag_name_exists'])
        return name


class NoteForm(forms.ModelForm):
    title = forms.CharField(min_length=5, max_length=255, required=True, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
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
        self.language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(self.language, translations['en'])
        self.fields['title'].widget.attrs.update({'placeholder': self.trans['enter_note_title']})
        self.fields['title'].label = self.trans['title']
        self.fields['content'].widget.attrs.update({'placeholder': self.trans['enter_note_content']})
        self.fields['content'].label = self.trans['content']
        self.fields['tags'].label = self.trans['tags']

    def clean_title(self):
        title = self.cleaned_data['title']
        if self.instance.pk:  # If the form edits an existing note
            if Note.objects.filter(user=self.user, title=title).exclude(pk=self.instance.pk).exists():
                raise ValidationError(self.trans['note_title_exists'])
        else:  # If this is a new note
            if Note.objects.filter(user=self.user, title=title).exists():
                raise ValidationError(self.trans['note_title_exists'])
        return title


class NoteSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
    )

    def __init__(self, *args, **kwargs):
        self.language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(self.language, translations['en'])
        self.fields['query'].widget.attrs.update({'placeholder': self.trans['search_field']})
