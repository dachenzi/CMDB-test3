from django.db import models

# Create your models here.

class Business(models.Model):

    title = models.CharField(max_length=32)


class Host(models.Model):

    hostname = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(protocol='ipv4')
    port = models.IntegerField()
    business = models.ForeignKey('Business')
