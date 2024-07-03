from django.contrib import admin
from .models import UserFile, Category


admin.site.register(Category)
admin.site.register(UserFile)
