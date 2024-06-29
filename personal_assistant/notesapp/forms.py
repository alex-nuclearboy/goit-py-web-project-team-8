from django import forms
from .models import Note, Tag
from django.core.exceptions import ValidationError
from .translations import translations


class TagForm(forms.ModelForm):
    """
    Form for creating and updating tags associated with a user.

    Fields:
    name (CharField): The name of the tag, with a minimum length of 3 and a maximum length of 25 characters.

    Methods:
    __init__(): Initializes the TagForm instance with user and language-specific translations.
    clean_name(): Validates that the tag name is unique for the user.
    """
    name = forms.CharField(min_length=3, max_length=25, required=True, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    class Meta:
        model = Tag
        fields = ['name']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, setting up user and language for translations.

        Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments, expecting 'user' and 'language'.
        """
        self.user = kwargs.pop('user', None)
        self.language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(self.language, translations['en'])
        self.fields['name'].widget.attrs.update({'placeholder': self.trans['enter_tag_name']})
        self.fields['name'].label = self.trans['tag_name']

    def clean_name(self):
        """
        Validates the 'name' field to ensure the tag name is unique for the user.

        Raises:
        ValidationError: If a tag with the same name already exists for the user.

        Returns:
        str: The cleaned name field.
        """
        name = self.cleaned_data['name']
        if Tag.objects.filter(user=self.user, name=name).exists():
            raise ValidationError(self.trans['tag_name_exists'])
        return name


class NoteForm(forms.ModelForm):
    """
    Form for creating and updating notes associated with a user.

    Fields:
    title (CharField): The title of the note, with a minimum length of 5 and a maximum length of 255 characters.
    content (CharField): The content of the note, with a minimum length of 5 and a maximum length of 255 characters.
    tags (ModelMultipleChoiceField): The tags associated with the note.

    Methods:
    __init__(): Initializes the NoteForm instance with user and language-specific translations.
    clean_title(): Validates that the note title is unique for the user.
    """
    title = forms.CharField(min_length=5, max_length=255, required=True, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    content = forms.CharField(min_length=5, max_length=255, required=False, widget=forms.Textarea(attrs={'rows': 4}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, setting up user and language for translations.

        Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments, expecting 'user' and 'language'.
        """
        self.user = kwargs.pop('user', None)
        self.language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(self.language, translations['en'])
        self.fields['tags'].queryset = Tag.objects.filter(user=self.user)
        self.fields['title'].widget.attrs.update({'placeholder': self.trans['enter_note_title']})
        self.fields['title'].label = self.trans['title']
        self.fields['content'].widget.attrs.update({'placeholder': self.trans['enter_note_content']})
        self.fields['content'].label = self.trans['content']
        self.fields['tags'].label = self.trans['tags']

    def clean_title(self):
        """
        Validates the 'title' field to ensure the note title is unique for the user.

        Raises:
        ValidationError: If a note with the same title already exists for the user.

        Returns:
        str: The cleaned title field.
        """
        title = self.cleaned_data['title']
        if self.instance.pk:
            if Note.objects.filter(user=self.user, title=title).exclude(pk=self.instance.pk).exists():
                raise ValidationError(self.trans['note_title_exists'])
        else:
            if Note.objects.filter(user=self.user, title=title).exists():
                raise ValidationError(self.trans['note_title_exists'])
        return title


class NoteSearchForm(forms.Form):
    """
    Form for searching notes associated with a user.

    Fields:
    query (CharField): The search query string, with a maximum length of 100 characters.

    Methods:
    __init__(): Initializes the NoteSearchForm instance with language-specific translations.
    """
    query = forms.CharField(
        required=False,
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, setting up language for translations.

        Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments, expecting 'language'.
        """
        self.language = kwargs.pop('language', 'en')
        super().__init__(*args, **kwargs)
        self.trans = translations.get(self.language, translations['en'])
        self.fields['query'].widget.attrs.update({'placeholder': self.trans['search_field']})


