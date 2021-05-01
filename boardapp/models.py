from django.db import models

# Create your models here.

class BoardModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    sns_image = models.ImageField(upload_to='')
    good = models.IntegerField(null=True, blank=True, default=0)
    readtext = models.TextField(null=True, blank=True, default='initial')

class FollowModel(models.Model):
    author = models.CharField(max_length=50)
    follow = models.IntegerField(null=True, blank=True, default=0)
    followtext = models.TextField(null=True, blank=True, default='initial')
    befollowed = models.IntegerField(null=True, blank=True, default=0)
    befollowedtext = models.TextField(null=True, blank=True, default='initial')
    