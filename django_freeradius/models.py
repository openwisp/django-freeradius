from django.db import models

# Create your models here.
class Radius_group(models.Model):
    id = models.UUIDField(primary_key=True, )
    groupname = models.CharField(max_length=255, unique=True)
    priority = models.IntegerField(default=1)
    creation date = models.DateField()
    modification date = models.DateField()
    notes = models.CharField()

class Radius_group_users(models.Model):
    username = models.CharField(max_length=64,unique=True,)
    id = models.UUIDField(primary_key=True, )
    groupname = models.CharField(max_length=255, unique=True)
    radius_replies = models.ManyToManyField('radius_replies', blank=True)
    radius_checks = models.ManyToManyField('Radcheck', blank=True)

class Radius_replies(models.Model):
    username = models.CharField(max_length=64)


class Radius_checks(model.Models):
    username = models.CharField(max_length=64)



class Radacct(models.Model):


class Nas(models.Model):
    nasname = models.CharField(max_length=128, unique=True, help_text='NAS Name (or IP address)')
    shortname = models.CharField(max_length=32)
    type = models.CharField(max_length=30, choices=NAS_TYPES)
    secret = models.CharField(max_length=60, help_text='Shared Secret')
    ports = models.IntegerField(blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
