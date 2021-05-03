from django.contrib import admin
from .models import BoardModel, ProfileModel

# Register your models here.

admin.site.register(BoardModel)
admin.site.register(ProfileModel)