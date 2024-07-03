from django.db import models
from django.contrib.auth import get_user_model

from cloudinary_storage.storage import RawMediaCloudinaryStorage

User = get_user_model()

class Category(models.Model):
    """
    Represents the structure category.

    Attributes:
    name (str): tag name up to 255 characters long.
    user (User): The user who owns the category.

    Methods:
    __str__(): Returns the name file for user.
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'name'], name='category_of_user')]

    def __str__(self):
        return self.name


class UserFile(models.Model):
    """
    Represents the structure of working with user files.

    Attributes:
    user (User): The user who owns the file.
    category (Category): The  category for user.
    file: user file 

    Methods:
    __str__(): Returns the name file for user.

    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(storage=RawMediaCloudinaryStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'file'], name='file_of_user')]

    def __str__(self):
        return f"{self.file.name}"
