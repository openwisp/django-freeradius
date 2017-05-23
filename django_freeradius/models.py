from django.db import models
# Create your models here.


class RadiusGroup(models.Model):
    id = models.UUIDField(primary_key=True)
    group_name = models.CharField(max_length=255, unique=True)
    priority = models.IntegerField(default=1)
    creation_date = models.DateField(null=True)
    modification_date = models.DateField(null=True)
    notes = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.group_name

    class Meta:
        ordering = ['group_name']


class RadiusGroupUsers(models.Model):
    username = models.CharField(max_length=64, unique=True)
    id = models.UUIDField(primary_key=True)
    group_name = models.CharField(max_length=255, unique=True)
    radius_replies = models.ManyToManyField('radius_replies', blank=True)
    radius_checks = models.ManyToManyField('Radcheck', blank=True)


class RadiusReplies(models.Model):
    username = models.CharField(max_length=64)
    value = models.CharField(max_length=40)
    op = models.CharField(max_length=2)
    attribute = models.CharField(max_length=64)


class RadiusChecks(models.Model):
    username = models.CharField(max_length=64)
    value = models.CharField(max_length=40)
    op = models.CharField(max_length=2)
    attribute = models.CharField(max_length=64)


class Radacct(models.Model):
    username = models.CharField(max_length=25, null=True)


class Nas(models.Model):
    NasName = models.CharField(max_length=128, unique=True, help_text='NAS Name (or IP address)')
    ShortName = models.CharField(max_length=32)
    type = models.CharField(max_length=30)
    secret = models.CharField(max_length=60, help_text='Shared Secret')
    ports = models.IntegerField(blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
