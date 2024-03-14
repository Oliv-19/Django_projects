from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Content(models.Model):
    content_id= models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    poster = models.ImageField(upload_to='media', max_length=100000, null=True)
    description = models.TextField(null=True)
    episodes = models.IntegerField(null=True)
    author = models.CharField(default=None, max_length=300, null=True)
    year = models.IntegerField(null=True)
    typeContent = models.CharField(max_length=100)

class User_Content(models.Model):
    user_id =models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, default=None, null=False)
    content_id =models.ForeignKey(Content, models.CASCADE,default=None, null=False)
    review = models.TextField(max_length=250)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.id)
    


    
    