from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Represents a tag associated with a user.

    Attributes:
    name (str): The name of the tag, with a maximum length of 50 characters.
    user (User): The user to whom the tag belongs.
    objects (Manager): The default manager for the model.

    Meta:
    constraints (list): Ensures that the combination of user and tag name is unique.

    Methods:
    __str__(): Returns the string representation of the tag.
    """
    name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'name'], name='tag_of_user')]

    def __str__(self):
        """
        Returns the string representation of the tag.

        Returns:
        str: The name of the tag.
        """
        return f"{self.name}"


class Note(models.Model):
    """
    Represents a note created by a user.

    Attributes:
    title (str): The title of the note, with a maximum length of 255 characters.
    content (str): The content of the note.
    tags (ManyToManyField): The tags associated with the note.
    user (User): The user who created the note.
    created_at (datetime): The date and time when the note was created.
    updated_at (datetime): The date and time when the note was last updated.
    objects (Manager): The default manager for the model.

    Meta:
    constraints (list): Ensures that the combination of user and note title is unique.

    Methods:
    __str__(): Returns the string representation of the note.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'title'], name='note_of_user')]

    def __str__(self):
        """
        Returns the string representation of the note.

        Returns:
        str: The title of the note.
        """
        return f'{self.title}'
