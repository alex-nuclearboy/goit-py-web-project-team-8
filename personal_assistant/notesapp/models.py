from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    objects = models.Manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'name'], name='tag_of_user')]

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    objects = models.Manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'title'], name='note_of_user')]

    def __str__(self):
        return self.title