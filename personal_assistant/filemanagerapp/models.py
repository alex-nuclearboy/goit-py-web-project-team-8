from django.db import models
from cloudinary.models import CloudinaryField, Category
from django.contrib.auth.models import User
from django import forms

# Create your models here.

# Советы Саши
# class Category(models.Model): 
#     name 
#     user
    
    
# class UploadedFile(models.Model):
#     category FK Category
#     file
#     url adress file
#     datetime
#     user


class UserFile(models.Model):
    
    """
    Represents the structure of working with user files.
    
    Attributes:
    user: The user who owns the tag.
    name (str): tag name up to 50 characters long.
    category (choices=CATEGORY_CHOICES): The default category for user.
    file: user file 
    
    Methods:
    __str__(): Returns the name file for user.
    
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    public_id = models.CharField(max_length=255, blank=True)
        
    objects = models.Manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'name', 'category', 'file'], name='file_of_user')]

    def __str__(self):
        return self.name    
    

class FileUploadForm(forms.ModelForm):
    
    """
    Represents the file upload structure
    
    """
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = UserFile
        fields = ['file', 'category', 'name']  
        

class Category(models.Model):
    
    """
    Represents the structure category.
    
    CATEGORY_CHOICES - Standard categories for all users

    Attributes:
    name (str): tag name up to 50 characters long.
    is_standard (choices=CATEGORY_CHOICES): The default category for user.
        
    Methods:
    __str__(): Returns the name file for user.
    
    """
    STANDARD_CATEGORIES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
    ]

    name = models.CharField(max_length=255, unique=True)
    is_standard = models.BooleanField(default=False)

    def __str__(self):
        return self.name