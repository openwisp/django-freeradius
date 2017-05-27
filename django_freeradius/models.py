from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class RadiusGroup(models.Model):
    id = models.UUIDField(primary_key=True)
    group_name = models.CharField(verbose_name=_('groupname'), max_length=255, unique=True)
    priority = models.IntegerField(verbose_name=_('priority'), default=1)
    creation_date = models.DateField(verbose_name=_('creation date'), null=True)
    modification_date = models.DateField(verbose_name=_('modification date'), null=True)
    notes = models.CharField(verbose_name=_('notes'), max_length=64, blank=True)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'radiusgroup'
        verbose_name = _("radiusgroup")
        verbose_name_plural = _("radiusgroups")


class RadiusGroupUsers(models.Model):
    user_name = models.CharField(verbose_name=_('username'), max_length=64, unique=True)
    id = models.UUIDField(primary_key=True)
    group_name = models.CharField(verbose_name=_('groupname'), max_length=255, unique=True)
    radius_replies = models.ManyToManyField('RadiusReplies', verbose_name=_('radius replies'), blank=True)
    radius_checks = models.ManyToManyField('RadiusChecks', verbose_name=_('radius checks'), blank=True)

    class Meta:
        db_table = 'radiusgroupusers'
        verbose_name = _("radiusgroupusers")
        verbose_name_plural = _("radiusgroupusers")

    def __str__(self):
        return self.user_name


class RadiusReplies(models.Model):
    user_name = models.CharField(verbose_name=_('username'), max_length=64)
    value = models.CharField(verbose_name=_('value'), max_length=40)
    op = models.CharField(verbose_name=_('op'), max_length=2)
    attribute = models.CharField(verbose_name=_('attribute'), max_length=64)

    class Meta:
        db_table = 'radiusreplies'
        verbose_name = _("radiusreplies")
        verbose_name_plural = _("radiusreplies")

    def __str__(self):
        return self.user_name


class RadiusChecks(models.Model):
    user_name = models.CharField(verbose_name=_('username'), max_length=64)
    value = models.CharField(verbose_name=_('radiusvalue'), max_length=40)
    op = models.CharField(verbose_name=_('op'), max_length=2)
    attribute = models.CharField(verbose_name=_('attribute'), max_length=64)

    class Meta:
        db_table = 'radiuschecks'
        verbose_name = _("radiuschecks")
        verbose_name_plural = _("radiuschecks")

    def __str__(self):
        return self.user_name


class RadiusAccounting(models.Model):
    rad_acct_id = models.BigIntegerField(primary_key=True)
    acct_session_id = models.CharField(max_length=32)
    acct_unique_id = models.CharField(max_length=32)
    user_name = models.CharField(verbose_name=_('username'), max_length=64)
    realm = models.CharField(verbose_name=_('realm'), max_length=64, null=True)
    nas_ip_address = models.CharField(max_length=15)
    nas_port_id = models.CharField(max_length=15, null=True)
    nas_port_type = models.CharField(verbose_name=_('nas port type'), max_length=32)
    acct_start_time = models.DateTimeField(verbose_name=_('acct start time'))
    acct_stop_time = models.DateTimeField(verbose_name=_('acct stop time'), null=True)
    acct_session_time = models.IntegerField(verbose_name=_('acct session time'), null=True)
    acct_authentic = models.CharField(verbose_name=_('acct authentic'), max_length=32, null=True)
    connection_info_start = models.CharField(
            verbose_name=_('connection info start'), max_length=50, null=True)
    connection_info_stop = models.CharField(verbose_name=_('connection info stop'), max_length=50, null=True)
    acct_input_octets = models.BigIntegerField(verbose_name=_('acct input octets'), null=True)
    acct_output_octets = models.BigIntegerField(verbose_name=_('acct output octets'), null=True)
    callingStationId = models.CharField(max_length=50)
    calledStationId = models.CharField(max_length=50)
    acct_terminate_cause = models.CharField(verbose_name=_('acct terminate cause'), max_length=32)
    service_type = models.CharField(verbose_name=_('service type'), max_length=32, null=True)
    framed_protocol = models.CharField(verbose_name=_('framed protocol'), max_length=32, null=True)
    framed_ip_address = models.CharField(max_length=15)
    acct_start_delay = models.IntegerField(verbose_name=_('acct start delay'), null=True)
    acct_stop_delay = models.IntegerField(verbose_name=_('acct stop delay'), null=True)
    xascend_session_svrkey = models.CharField(
            verbose_name=_('xascend session svrkey'), max_length=10, null=True)

    class Meta:
        db_table = 'radiusaccounting'
        verbose_name = _("radiusaccounting")
        verbose_name_plural = _("radiusaccounting")

    def __str__(self):
        return self.acct_unique_id


class Nas(models.Model):
    nas_name = models.CharField(
            verbose_name=_('nas name'), max_length=128, unique=True, help_text=_('NAS Name (or IP address)'))
    short_name = models.CharField(verbose_name=_('short name'), max_length=32)
    type = models.CharField(verbose_name=_('type'), max_length=30)
    secret = models.CharField(verbose_name=_('secret'), max_length=60, help_text=_('Shared Secret'))
    ports = models.IntegerField(verbose_name=_('ports'), blank=True, null=True)
    community = models.CharField(verbose_name=_('community'), max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'nas'
        verbose_name = _("nas")
        verbose_name_plural = _("nas")

    def __str__(self):
        return self.nas_name
