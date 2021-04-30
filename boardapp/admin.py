from django.contrib import admin
from .models import BoardModel, FollowModel

# Register your models here.

admin.site.register(BoardModel)
admin.site.register(FollowModel)