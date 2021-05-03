from django.db import models

# Create your models here.

class BoardModel(models.Model):
    user_id = models.IntegerField(null=True, blank=True, default=0)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    sns_image = models.ImageField(upload_to='',null=True, blank=True, default=0)
    good = models.IntegerField(null=True, blank=True, default=0)
    readtext = models.TextField(null=True, blank=True, default='initial')

class ProfileModel(models.Model):
    user_id = models.IntegerField(null=True, blank=True, default=0)
    author = models.CharField(max_length=50)
    one_thing = models.TextField(null=True, blank=True, default='initial')
    header_image = models.ImageField(upload_to='', null=True, blank=True, default=0)
    follow_number = models.IntegerField(null=True, blank=True, default=0)
    follow_text = models.TextField(null=True, blank=True, default='initial')
    befollowed_number = models.IntegerField(null=True, blank=True, default=0)
    befollowed_text = models.TextField(null=True, blank=True, default='initial')
