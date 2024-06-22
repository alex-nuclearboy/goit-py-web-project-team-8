from django.db import models
from django.contrib.auth.models import User
from .storage_avatar import LocalStorage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default='default_avatar.png',
        upload_to='profile_images',
        storage=LocalStorage()
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.avatar and not self._state.adding:
            super().save(*args, **kwargs)  # Save the instance before resizing

            img = Image.open(self.avatar)
            if img.height > 250 or img.width > 250:
                output = BytesIO()

                # Use Resampling.LANCZOS for high-quality downsampling
                img.thumbnail((250, 250), Image.Resampling.LANCZOS)

                # Determine the format based on the file extension
                img_format = (
                    'PNG' if 'png' in self.avatar.name.lower() else 'JPEG'
                )
                img.save(output, format=img_format)
                output.seek(0)

                # Save the resized image back to the avatar field
                self.avatar.save(
                    self.avatar.name,
                    ContentFile(output.getvalue()),
                    save=False
                )

            super().save(*args, **kwargs)  # Save the instance again
        else:
            super().save(*args, **kwargs)
