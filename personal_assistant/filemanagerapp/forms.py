from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name']

    

# class FileForm(forms.ModelForm):    
#     class Meta:
#         fields = ("",)
    
#     Categoriy
#     file    


