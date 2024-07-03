from django import forms
from .models import Category, UserFile

from .translations import translations


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, user, language, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.trans = translations.get(language, translations['en'])
        self.fields['name'].label = self.trans['category_name']
        self.fields['name'].widget.attrs.update({
            'placeholder': self.trans['category_name_placeholder'],
            'class': 'form-control'
        })


class FileUploadForm(forms.ModelForm):
    """
    Represents the file upload structure
    """
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)

    class Meta:
        model = UserFile
        fields = ['file', 'category']

    def __init__(self, user, language, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.trans = translations.get(language, translations['en'])
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['category'].label = ''
        self.fields['file'].label = self.trans['file']

        translated_categories = {
            'Uncategorised': self.trans.get('uncategorised', 'Uncategorised'),
            'Photos': self.trans.get('photos', 'Photos'),
            'Videos': self.trans.get('videos', 'Videos'),
            'Music': self.trans.get('music', 'Music'),
            'Documents': self.trans.get('documents', 'Documents'),
            'Archives': self.trans.get('archives', 'Archives'),
            'Other': self.trans.get('other', 'Other')
        }
        self.fields['category'].choices = [
            (category.id, translated_categories.get(category.name, category.name))
            for category in self.fields['category'].queryset
        ]


class EditFileCategoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, user, language, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = translations.get(language, translations['en'])
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['category'].label = ''

        translated_categories = {
            'Uncategorised': self.trans.get('uncategorised', 'Uncategorised'),
            'Photos': self.trans.get('photos', 'Photos'),
            'Videos': self.trans.get('videos', 'Videos'),
            'Music': self.trans.get('music', 'Music'),
            'Documents': self.trans.get('documents', 'Documents'),
            'Archives': self.trans.get('archives', 'Archives'),
            'Other': self.trans.get('other', 'Other')
        }
        self.fields['category'].choices = [
            (category.id, translated_categories.get(category.name, category.name))
            for category in self.fields['category'].queryset
        ]

    class Meta:
        model = UserFile
        fields = ['category']
