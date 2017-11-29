from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

RADOP_CHECK_TYPES = (
    ('=', '='),
    (':=', ':='),
    ('==', '=='),
    ('+=', '+='),
    ('!=', '!='),
    ('>', '>'),
    ('>=', '>='),
    ('<', '<'),
    ('<=', '<='),
    ('=~', '=~'),
    ('!~', '!~'),
    ('=*', '=*'),
    ('!*', '!*'),
)

RADOP_REPLY_TYPES = (
    ('=', '='),
    (':=', ':='),
    ('+=', '+='),
)

RADCHECK_PASSWD_TYPE = (
    ('Cleartext-Password', 'Cleartext-Password'),
    ('NT-Password', 'NT-Password'),
    ('LM-Password', 'LM-Password'),
    ('MD5-Password', 'MD5-Password'),
    ('SMD5-Password', 'SMD5-Password'),
    ('SSHA-Password', 'SSHA-Password'),
    ('Crypt-Password', 'Crypt-Password'),
)


class TimeStampedEditableModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = AutoCreatedField(_('created'), editable=True)
    modified = AutoLastModifiedField(_('modified'), editable=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class AbstractRadiusGroup(TimeStampedEditableModel):
    id = models.UUIDField(primary_key=True, db_column='id')
    groupname = models.CharField(verbose_name=_('group name'),
                                 max_length=255,
                                 unique=True,
                                 db_index=True)
    priority = models.IntegerField(verbose_name=_('priority'), default=1)
    notes = models.CharField(verbose_name=_('notes'),
                             max_length=64,
                             blank=True,
                             null=True)

    class Meta:
        db_table = 'radiusgroup'
        verbose_name = _('radius group')
        verbose_name_plural = _('radius groups')
        abstract = True

    def __str__(self):
        return self.groupname


@python_2_unicode_compatible
class AbstractRadiusGroupUsers(TimeStampedEditableModel):
    id = models.UUIDField(primary_key=True,
                          db_column='id')
    username = models.CharField(verbose_name=_('username'),
                                max_length=64,
                                unique=True)
    groupname = models.CharField(verbose_name=_('group name'),
                                 max_length=255,
                                 unique=True)
    radius_reply = models.ManyToManyField('RadiusReply',
                                          verbose_name=_('radius reply'),
                                          blank=True,
                                          db_column='radiusreply')
    radius_check = models.ManyToManyField('RadiusCheck',
                                          verbose_name=_('radius check'),
                                          blank=True,
                                          db_column='radiuscheck')

    class Meta:
        db_table = 'radiusgroupusers'
        verbose_name = _('radius group users')
        verbose_name_plural = _('radius group users')
        abstract = True

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class AbstractRadiusReply(TimeStampedEditableModel):
    username = models.CharField(verbose_name=_('username'),
                                max_length=64,
                                db_index=True)
    value = models.CharField(verbose_name=_('value'), max_length=253)
    op = models.CharField(verbose_name=_('operator'),
                          max_length=2,
                          choices=RADOP_REPLY_TYPES,
                          default='=')
    attribute = models.CharField(verbose_name=_('attribute'), max_length=64)

    class Meta:
        db_table = 'radreply'
        verbose_name = _('radius reply')
        verbose_name_plural = _('radius replies')
        abstract = True

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class AbstractRadiusCheck(TimeStampedEditableModel):
    username = models.CharField(verbose_name=_('username'),
                                max_length=64,
                                db_index=True)
    value = models.CharField(verbose_name=_('value'), max_length=253)
    op = models.CharField(verbose_name=_('operator'),
                          max_length=2,
                          choices=RADOP_CHECK_TYPES,
                          default=':=')
    attribute = models.CharField(verbose_name=_('attribute'),
                                 max_length=64,
                                 choices=RADCHECK_PASSWD_TYPE)
    is_active = models.BooleanField(default=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'radcheck'
        verbose_name = _('radius check')
        verbose_name_plural = _('radius checks')
        abstract = True

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class AbstractRadiusAccounting(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='radacctid')
    session_id = models.CharField(verbose_name=_('session ID'),
                                  max_length=64,
                                  db_column='acctsessionid',
                                  db_index=True)
    unique_id = models.CharField(verbose_name=_('accounting unique ID'),
                                 max_length=32,
                                 db_column='acctuniqueid',
                                 unique=True)
    username = models.CharField(verbose_name=_('username'),
                                max_length=64,
                                db_index=True,
                                null=True,
                                blank=True)
    groupname = models.CharField(verbose_name=_('group name'),
                                 max_length=64,
                                 null=True,
                                 blank=True)
    realm = models.CharField(verbose_name=_('realm'),
                             max_length=64,
                             null=True,
                             blank=True)
    nas_ip_address = models.GenericIPAddressField(verbose_name=_('NAS IP address'),
                                                  db_column='nasipaddress',
                                                  db_index=True)
    nas_port_id = models.CharField(verbose_name=_('NAS port ID'),
                                   max_length=15,
                                   db_column='nasportid',
                                   null=True,
                                   blank=True)
    nas_port_type = models.CharField(verbose_name=_('NAS port type'),
                                     max_length=32,
                                     db_column='nasporttype',
                                     null=True,
                                     blank=True)
    start_time = models.DateTimeField(verbose_name=_('start time'),
                                      db_column='acctstarttime',
                                      db_index=True,
                                      null=True,
                                      blank=True)
    update_time = models.DateTimeField(verbose_name=_('update time'),
                                       db_column='acctupdatetime',
                                       null=True,
                                       blank=True)
    stop_time = models.DateTimeField(verbose_name=_('stop time'),
                                     db_column='acctstoptime',
                                     db_index=True,
                                     null=True,
                                     blank=True)
    interval = models.IntegerField(verbose_name=_('interval'),
                                   db_column='acctinterval',
                                   null=True,
                                   blank=True)
    session_time = models.PositiveIntegerField(verbose_name=_('session time'),
                                               db_column='acctsessiontime',
                                               null=True,
                                               blank=True)
    authentication = models.CharField(verbose_name=_('authentication'),
                                      max_length=32,
                                      db_column='acctauthentic',
                                      null=True,
                                      blank=True)
    connection_info_start = models.CharField(verbose_name=_('connection info start'),
                                             max_length=50,
                                             db_column='connectinfo_start',
                                             null=True,
                                             blank=True)
    connection_info_stop = models.CharField(verbose_name=_('connection info stop'),
                                            max_length=50,
                                            db_column='connectinfo_stop',
                                            null=True,
                                            blank=True)
    input_octets = models.BigIntegerField(verbose_name=_('input octets'),
                                          db_column='acctinputoctets',
                                          null=True,
                                          blank=True)
    output_octets = models.BigIntegerField(verbose_name=_('output octets'),
                                           db_column='acctoutputoctets',
                                           null=True,
                                           blank=True)
    called_station_id = models.CharField(verbose_name=_('called station ID'),
                                         max_length=50,
                                         db_column='calledstationid',
                                         blank=True,
                                         null=True)
    calling_station_id = models.CharField(verbose_name=_('calling station ID'),
                                          max_length=50,
                                          db_column='callingstationid',
                                          blank=True,
                                          null=True)
    terminate_cause = models.CharField(verbose_name=_('termination cause'),
                                       max_length=32,
                                       db_column='acctterminatecause',
                                       blank=True,
                                       null=True)
    service_type = models.CharField(verbose_name=_('service type'),
                                    max_length=32,
                                    db_column='servicetype',
                                    null=True,
                                    blank=True)
    framed_protocol = models.CharField(verbose_name=_('framed protocol'),
                                       max_length=32,
                                       db_column='framedprotocol',
                                       null=True,
                                       blank=True)
    framed_ip_address = models.GenericIPAddressField(verbose_name=_('framed IP address'),
                                                     db_column='framedipaddress',
                                                     db_index=True,
                                                     # the default MySQL freeradius schema defines
                                                     # this as NOT NULL but defaulting to empty string
                                                     # but that wouldn't work on PostgreSQL
                                                     null=True,
                                                     blank=True)

    def save(self, *args, **kwargs):
        if not self.start_time:
            self.start_time = now()
        super(AbstractRadiusAccounting, self).save(*args, **kwargs)

    class Meta:
        db_table = 'radacct'
        verbose_name = _('accounting')
        verbose_name_plural = _('accountings')
        abstract = True

    def __str__(self):
        return self.unique_id


@python_2_unicode_compatible
class AbstractNas(TimeStampedEditableModel):
    name = models.CharField(verbose_name=_('name'),
                            max_length=128,
                            help_text=_('NAS Name (or IP address)'),
                            db_index=True,
                            db_column='nasname')
    short_name = models.CharField(verbose_name=_('short name'),
                                  max_length=32,
                                  db_column='shortname')
    type = models.CharField(verbose_name=_('type'),
                            max_length=30,
                            default='other')
    ports = models.PositiveIntegerField(verbose_name=_('ports'),
                                        blank=True,
                                        null=True)
    secret = models.CharField(verbose_name=_('secret'),
                              max_length=60,
                              help_text=_('Shared Secret'))
    server = models.CharField(verbose_name=_('server'),
                              max_length=64,
                              blank=True,
                              null=True)
    community = models.CharField(verbose_name=_('community'),
                                 max_length=50,
                                 blank=True,
                                 null=True)
    description = models.CharField(verbose_name=_('description'),
                                   max_length=200,
                                   null=True,
                                   blank=True)

    class Meta:
        db_table = 'nas'
        verbose_name = _('NAS')
        verbose_name_plural = _('NAS')
        abstract = True

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AbstractRadiusUserGroup(TimeStampedEditableModel):
    username = models.CharField(verbose_name=_('username'),
                                max_length=64,
                                db_index=True)
    groupname = models.CharField(verbose_name=_('group name'),
                                 max_length=64)
    priority = models.IntegerField(verbose_name=_('priority'), default=1)

    class Meta:
        db_table = 'radusergroup'
        verbose_name = _('radius user group association')
        verbose_name_plural = _('radius user group associations')
        abstract = True

    def __str__(self):
        return str(self.username)


@python_2_unicode_compatible
class AbstractRadiusGroupReply(TimeStampedEditableModel):
    groupname = models.CharField(verbose_name=_('group name'),
                                 max_length=64,
                                 db_index=True)
    attribute = models.CharField(verbose_name=_('attribute'), max_length=64)
    op = models.CharField(verbose_name=_('operator'),
                          max_length=2,
                          choices=RADOP_REPLY_TYPES,
                          default='=')
    value = models.CharField(verbose_name=_('value'), max_length=253)

    class Meta:
        db_table = 'radgroupreply'
        verbose_name = _('radius group reply')
        verbose_name_plural = _('radius group replies')
        abstract = True

    def __str__(self):
        return str(self.groupname)


@python_2_unicode_compatible
class AbstractRadiusGroupCheck(TimeStampedEditableModel):
    groupname = models.CharField(verbose_name=_('group name'),
                                 max_length=64,
                                 db_index=True)
    attribute = models.CharField(verbose_name=_('attribute'), max_length=64)
    op = models.CharField(verbose_name=_('operator'),
                          max_length=2,
                          choices=RADOP_CHECK_TYPES,
                          default=':=')
    value = models.CharField(verbose_name=_('value'), max_length=253)

    class Meta:
        db_table = 'radgroupcheck'
        verbose_name = _('radius group check')
        verbose_name_plural = _('radius group checks')
        abstract = True

    def __str__(self):
        return str(self.groupname)


@python_2_unicode_compatible
class AbstractRadiusPostAuth(models.Model):
    username = models.CharField(verbose_name=_('username'),
                                max_length=64)
    password = models.CharField(verbose_name=_('password'),
                                max_length=64,
                                db_column='pass',
                                blank=True)
    reply = models.CharField(verbose_name=_('reply'),
                             max_length=32)
    called_station_id = models.CharField(verbose_name=_('called station ID'),
                                         max_length=50,
                                         db_column='calledstationid',
                                         blank=True,
                                         null=True)
    calling_station_id = models.CharField(verbose_name=_('calling station ID'),
                                          max_length=50,
                                          db_column='callingstationid',
                                          blank=True,
                                          null=True)
    date = models.DateTimeField(verbose_name=_('date'),
                                db_column='authdate',
                                auto_now_add=True)

    class Meta:
        db_table = 'radpostauth'
        verbose_name = _('radius post authentication log')
        verbose_name_plural = _('radius post authentication logs')
        abstract = True

    def __str__(self):
        return str(self.username)
