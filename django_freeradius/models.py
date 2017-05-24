from django.db import models


# Create your models here.


class RadiusGroup(models.Model):
    id = models.UUIDField(primary_key=True)
    group_name = models.CharField(max_length=255, unique=True)
    priority = models.IntegerField(default=1)
    creation_date = models.DateField(null=True)
    modification_date = models.DateField(null=True)
    notes = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'radiusgroup'


class RadiusGroupUsers(models.Model):
    user_name = models.CharField(max_length=64, unique=True)
    id = models.UUIDField(primary_key=True)
    group_name = models.CharField(max_length=255, unique=True)
    radius_replies = models.ManyToManyField('RadiusReplies', blank=True)
    radius_checks = models.ManyToManyField('RadiusChecks', blank=True)

    class Meta:
        db_table = 'radiusgroupusers'

    def __str__(self):
        return self.user_name


class RadiusReplies(models.Model):
    user_name = models.CharField(max_length=64)
    value = models.CharField(max_length=40)
    op = models.CharField(max_length=2)
    attribute = models.CharField(max_length=64)

    class Meta:
        db_table = 'radiusreplies'

    def __str__(self):
        return self.user_name


class RadiusChecks(models.Model):
    user_name = models.CharField(max_length=64)
    value = models.CharField(max_length=40)
    op = models.CharField(max_length=2)
    attribute = models.CharField(max_length=64)

    class Meta:
        db_table = 'radiuschecks'

    def __str__(self):
        return self.user_name


class RadiusAccounting(models.Model):
    rad_acct_id = models.BigIntegerField(primary_key=True)
    acct_session_id = models.CharField(max_length=32)
    acct_unique_id = models.CharField(max_length=32)
    user_name = models.CharField(max_length=64)
    realm = models.CharField(max_length=64, null=True)
    nas_ip_address = models.CharField(max_length=15)
    nas_port_id = models.CharField(max_length=15, null=True)
    nas_port_type = models.CharField(max_length=32)
    acct_start_time = models.DateTimeField()
    acct_stop_time = models.DateTimeField(null=True)
    acct_session_time = models.IntegerField(null=True)
    acct_authentic = models.CharField(max_length=32, null=True)
    connection_info_start = models.CharField(max_length=50, null=True)
    connection_info_stop = models.CharField(max_length=50, null=True)
    acct_input_octets = models.BigIntegerField(null=True)
    acct_output_octets = models.BigIntegerField(null=True)
    callingStationId = models.CharField(max_length=50)
    calledStationId = models.CharField(max_length=50)
    acct_terminate_cause = models.CharField(max_length=32)
    service_type = models.CharField(max_length=32, null=True)
    framed_protocol = models.CharField(max_length=32, null=True)
    framed_ip_address = models.CharField(max_length=15)
    acct_start_delay = models.IntegerField(null=True)
    acct_stop_delay = models.IntegerField(null=True)
    xascend_session_svrkey = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'radiusaccounting'

    def __str__(self):
        return self.acct_unique_id


class Nas(models.Model):
    nas_name = models.CharField(max_length=128, unique=True, help_text='NAS Name (or IP address)')
    short_name = models.CharField(max_length=32)
    type = models.CharField(max_length=30)
    secret = models.CharField(max_length=60, help_text='Shared Secret')
    ports = models.IntegerField(blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'nas'

    def __str__(self):
        return self.nas_name
