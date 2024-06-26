from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'name'], name='tag_of_user')]

    def __str__(self):
        return f'{self.name}'


class Note(models.Model):
    title = models.CharField(max_length=255, null=False)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'title'], name='note_of_user')]

    def __str__(self):
        return f'{self.title}'
