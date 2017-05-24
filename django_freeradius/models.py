from django.db import models
# Create your models here.


class RadiusGroup(models.Model):
    id = models.UUIDField(primary_key=True)
    groupName = models.CharField(max_length=255, unique=True)
    priority = models.IntegerField(default=1)
    creationDate = models.DateField(null=True)
    modificationDate = models.DateField(null=True)
    notes = models.CharField(max_length=64, blank=True)


class RadiusGroupUsers(models.Model):
    userName = models.CharField(max_length=64, unique=True)
    id = models.UUIDField(primary_key=True)
    groupName = models.CharField(max_length=255, unique=True)
    radiusReplies = models.ManyToManyField('RadiusReplies', blank=True)
    radiusChecks = models.ManyToManyField('RadiusChecks', blank=True)


class RadiusReplies(models.Model):
    userName = models.CharField(max_length=64)
    value = models.CharField(max_length=40)
    op = models.CharField(max_length=2)
    attribute = models.CharField(max_length=64)


class RadiusChecks(models.Model):
    userName = models.CharField(max_length=64)
    value = models.CharField(max_length=40)
    op = models.CharField(max_length=2)
    attribute = models.CharField(max_length=64)


class RadiusAccounting(models.Model):
    radAcctId = models.BigIntegerField(primary_key=True)
    acctSessionId = models.CharField(max_length=32)
    acctUniqueId = models.CharField(max_length=32)
    userName = models.CharField(max_length=64)
    realm = models.CharField(max_length=64, null=True)
    nasIpAddress = models.CharField(max_length=15)
    nasPortId = models.CharField(max_length=15, null=True)
    nasPortType = models.CharField(max_length=32)
    acctStartTime = models.DateTimeField()
    acctStopTime = models.DateTimeField(null=True)
    acctSessionTime = models.IntegerField(null=True)
    acctAuthentic = models.CharField(max_length=32, null=True)
    connectionInfoStart = models.CharField(max_length=50, null=True)
    connectionInfoStop = models.CharField(max_length=50, null=True)
    acctInputOctets = models.BigIntegerField(null=True)
    acctOutputOctets = models.BigIntegerField(null=True)
    callingStationId = models.CharField(max_length=50)
    calledStationId = models.CharField(max_length=50)
    acctTerminateCause = models.CharField(max_length=32)
    serviceType = models.CharField(max_length=32, null=True)
    framedProtocol = models.CharField(max_length=32, null=True)
    framedIpAddress = models.CharField(max_length=15)
    acctStartDelay = models.IntegerField(null=True)
    acctStopDelay = models.IntegerField(null=True)
    xAscendSessionSvrKey = models.CharField(max_length=10, null=True)


class Nas(models.Model):
    nasName = models.CharField(max_length=128, unique=True, help_text='NAS Name (or IP address)')
    shortName = models.CharField(max_length=32)
    type = models.CharField(max_length=30)
    secret = models.CharField(max_length=60, help_text='Shared Secret')
    ports = models.IntegerField(blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
