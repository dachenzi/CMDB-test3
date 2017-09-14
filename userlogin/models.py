from django.db import models
import hostmanager.models

# Create your models here.


class User(models.Model):

    username = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    email = models.EmailField()
    role = models.ForeignKey('Role')
    adminhost = models.ManyToManyField(hostmanager.models.Host)


class Role(models.Model):

    role_name = models.CharField(max_length=8)