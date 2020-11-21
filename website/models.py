from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_random_queryset import RandomManager
from PIL import Image
import os
# Create your models here.


class Profile(models.Model):
    objects = RandomManager()
    sno = models.IntegerField(primary_key=True)
    profile_pic = models.ImageField(default="profile-logo.png")
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    name = models.CharField(max_length=255,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    desc = models.TextField(default="Hey There! I'm using CLGin")
    linkedin = models.URLField(max_length=200,blank=True)
    fb = models.URLField(max_length=200,blank=True)
    ig = models.URLField(max_length=200,blank=True)
    phone = models.IntegerField(max_length=13,blank=True,null=True,default=9999999999)
    is_phone = models.BooleanField(blank=True,default=0)
    year = models.CharField(max_length=10,default="FE")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        if img.height > 200 or img.width>200:
            output_size= (200,200)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    def __str__(self):
        return self.name

class Skills(models.Model):

    id = models.IntegerField(primary_key=True)
    skill = models.CharField(max_length=255,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + self.skill

class Education(models.Model):
    name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    span = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    def __str__(self):
        return self.user.username + ' ' + self.name[0:5]

class work(models.Model):
    name = models.CharField(max_length=255)
    work = models.CharField(max_length=255)
    span = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)

class achievement(models.Model):
    id = models.IntegerField(primary_key=True)
    achievement = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Notification(models.Model):
    id = models.IntegerField(primary_key=True)
    notification = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + ' ' + self.notification