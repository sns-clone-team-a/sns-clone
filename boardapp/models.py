from django.db import models

# Create your models here.

class BoardModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    sns_image = models.ImageField(upload_to='',null=True, blank=True, default=0)
    good = models.IntegerField(null=True, blank=True, default=0)
    readtext = models.TextField(null=True, blank=True, default='initial')

class ProfileModel(models.Model):
    author = models.CharField(max_length=50)
    one_thing = models.TextField()
    header_image = models.ImageField(upload_to='')
    follow_number = models.IntegerField(null=True, blank=True, default=0)
    follow_text = models.TextField(null=True, blank=True, default='initial')
    befollowed_number = models.IntegerField(null=True, blank=True, default=0)
    befollowed_text = models.TextField(null=True, blank=True, default='initial')