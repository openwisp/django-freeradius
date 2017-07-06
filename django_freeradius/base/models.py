from django.db import models
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


class TimeStampedEditableModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = AutoCreatedField(_('created'), editable=True)
    modified = AutoLastModifiedField(_('modified'), editable=True)

    class Meta:
        abstract = True


class AbstractRadiusGroup(TimeStampedEditableModel):
    id = models.UUIDField(primary_key=True, db_column='id')
    group_name = models.CharField(verbose_name=_('groupname'),
                                  max_length=255,
                                  unique=True,
                                  db_column='groupname',
                                  db_index=True)
    priority = models.IntegerField(verbose_name=_('priority'), default=1)
    creation_date = models.DateField(verbose_name=_('creation date'),
                                     null=True,
                                     db_column='created_at')
    modification_date = models.DateField(verbose_name=_('modification date'),
                                         null=True,
                                         db_column='updated_at')
    notes = models.CharField(verbose_name=_('notes'),
                             max_length=64,
                             blank=True,
                             null=True)

    class Meta:
        db_table = 'radiusgroup'
        verbose_name = _('radiusgroup')
        verbose_name_plural = _('radiusgroups')
        abstract = True

    def __str__(self):
        return self.group_name


class AbstractRadiusGroupUsers(TimeStampedEditableModel):
    id = models.UUIDField(primary_key=True,
                          db_column='id')
    user_name = models.CharField(verbose_name=_('username'),
                                 max_length=64,
                                 unique=True,
                                 db_column='username')
    group_name = models.CharField(verbose_name=_('groupname'),
                                  max_length=255,
                                  unique=True,
                                  db_column='groupname')
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
        verbose_name = _('radiusgroupusers')
        verbose_name_plural = _('radiusgroupusers')
        abstract = True

    def __str__(self):
        return self.user_name


class AbstractRadiusReply(TimeStampedEditableModel):
    user_name = models.CharField(verbose_name=_('username'),
                                 max_length=64,
                                 db_column='username',
                                 db_index=True)
    value = models.CharField(verbose_name=_('value'), max_length=253)
    op = models.CharField(verbose_name=_('operator'),
                          max_length=2,
                          choices=RADOP_REPLY_TYPES,
                          default='=')
    attribute = models.CharField(verbose_name=_('attribute'), max_length=64)

    class Meta:
        db_table = 'radreply'
        verbose_name = _('radiusreply')
        verbose_name_plural = _('radiusreplies')
        abstract = True

    def __str__(self):
        return self.user_name


class AbstractRadiusCheck(TimeStampedEditableModel):
    user_name = models.CharField(verbose_name=_('username'),
                                 max_length=64,
                                 db_column='username',
                                 db_index=True)
    value = models.CharField(verbose_name=_('radiusvalue'), max_length=253)
    op = models.CharField(verbose_name=_('operator'),
                          max_length=2,
                          choices=RADOP_CHECK_TYPES,
                          default=':=')
    attribute = models.CharField(verbose_name=_('attribute'),
                                 max_length=64)

    class Meta:
        db_table = 'radcheck'
        verbose_name = _('radiuscheck')
        verbose_name_plural = _('radiuschecks')
        abstract = True

    def __str__(self):
        return self.user_name


class AbstractRadiusAccounting(TimeStampedEditableModel):
    rad_acct_id = models.BigIntegerField(primary_key=True, db_column='radacctid')
    acct_session_id = models.CharField(max_length=64,
                                       db_column='acctsessionid',
                                       db_index=True)
    acct_unique_id = models.CharField(max_length=32,
                                      db_column='acctuniqueid',
                                      unique=True)
    user_name = models.CharField(verbose_name=_('username'),
                                 max_length=64,
                                 db_column='username',
                                 db_index=True)
    group_name = models.CharField(verbose_name=_('groupname'),
                                  max_length=64,
                                  db_column='groupname')
    realm = models.CharField(verbose_name=_('realm'),
                             max_length=64,
                             null=True)
    nas_ip_address = models.CharField(max_length=15,
                                      db_column='nasipaddress',
                                      db_index=True)
    nas_port_id = models.CharField(max_length=15,
                                   null=True,
                                   db_column='nasportid')
    nas_port_type = models.CharField(verbose_name=_('nas port type'),
                                     max_length=32,
                                     db_column='nasporttype')
    acct_start_time = models.DateTimeField(verbose_name=_('acct start time'),
                                           db_column='acctstarttime',
                                           db_index=True)
    acct_stop_time = models.DateTimeField(verbose_name=_('acct stop time'),
                                          null=True,
                                          db_column='acctstoptime',
                                          db_index=True)
    acct_session_time = models.IntegerField(verbose_name=_('acct session time'),
                                            null=True,
                                            db_column='acctsessiontime',
                                            db_index=True)
    acct_authentic = models.CharField(verbose_name=_('acct authentic'),
                                      max_length=32,
                                      null=True,
                                      db_column='acctauthentic')
    connection_info_start = models.CharField(verbose_name=_('connection info start'),
                                             max_length=50,
                                             null=True,
                                             db_column='connectinfo_start')
    connection_info_stop = models.CharField(verbose_name=_('connection info stop'),
                                            max_length=50,
                                            null=True,
                                            db_column='connectinfo_stop')
    acct_input_octets = models.BigIntegerField(verbose_name=_('acct input octets'),
                                               null=True,
                                               db_column='acctinputoctets')
    acct_output_octets = models.BigIntegerField(verbose_name=_('acct output octets'),
                                                null=True,
                                                db_column='acctoutputoctets')
    callingStationId = models.CharField(max_length=50,
                                        db_column='calledstationid')
    calledStationId = models.CharField(max_length=50,
                                       db_column='callingstationid')
    acct_terminate_cause = models.CharField(verbose_name=_('acct terminate cause'),
                                            max_length=32,
                                            db_column='acctterminatecause')
    service_type = models.CharField(verbose_name=_('service type'),
                                    max_length=32,
                                    null=True,
                                    db_column='servicetype')
    framed_protocol = models.CharField(verbose_name=_('framed protocol'),
                                       max_length=32,
                                       null=True,
                                       db_column='framedprotocol')
    framed_ip_address = models.CharField(max_length=15,
                                         db_column='framedipaddress',
                                         db_index=True)
    acct_start_delay = models.IntegerField(verbose_name=_('acct start delay'),
                                           null=True,
                                           db_column='acctstartdelay')
    acct_stop_delay = models.IntegerField(verbose_name=_('acct stop delay'),
                                          null=True,
                                          db_column='acctstopdelay')
    xascend_session_svrkey = models.CharField(verbose_name=_('xascend session svrkey'),
                                              max_length=10,
                                              null=True,
                                              db_column='xascendsessionsvrkey')

    class Meta:
        db_table = 'radacct'
        verbose_name = _('accounting')
        verbose_name_plural = _('accounting')
        abstract = True

    def __str__(self):
        return self.acct_unique_id


class AbstractNas(TimeStampedEditableModel):
    nas_name = models.CharField(verbose_name=_('nas name'),
                                max_length=128,
                                unique=True,
                                help_text=_('NAS Name (or IP address)'),
                                db_index=True,
                                db_column='nasname')
    short_name = models.CharField(verbose_name=_('short name'),
                                  max_length=32,
                                  db_column='shortname')
    type = models.CharField(verbose_name=_('type'), max_length=30)
    secret = models.CharField(verbose_name=_('secret'),
                              max_length=60,
                              help_text=_('Shared Secret'))
    ports = models.IntegerField(verbose_name=_('ports'),
                                blank=True,
                                null=True)
    community = models.CharField(verbose_name=_('community'),
                                 max_length=50,
                                 blank=True,
                                 null=True)
    description = models.CharField(verbose_name=_('description'),
                                   max_length=200,
                                   null=True)
    server = models.CharField(verbose_name=_('server'),
                              max_length=64,
                              null=True)

    class Meta:
        db_table = 'nas'
        verbose_name = _('nas')
        verbose_name_plural = _('nas')
        abstract = True

    def __str__(self):
        return self.nas_name


class AbstractRadiusUserGroup(TimeStampedEditableModel):
    user_name = models.CharField(verbose_name=_('username'),
                                 max_length=64,
                                 db_column='username',
                                 db_index=True)
    group_name = models.CharField(verbose_name=_('groupname'),
                                  max_length=64,
                                  db_column='groupname')
    priority = models.IntegerField(verbose_name=_('priority'), default=1)

    class Meta:
        db_table = 'radusergroup'
        verbose_name = _('radiususergroup')
        verbose_name_plural = _('radiususergroup')
        abstract = True

    def __str__(self):
        return str(self.user_name)


class AbstractRadiusGroupReply(TimeStampedEditableModel):
    group_name = models.CharField(verbose_name=_('groupname'),
                                  max_length=64,
                                  db_column='groupname',
                                  db_index=True)
    attribute = models.CharField(verbose_name=_('attribute'), max_length=64)
    op = models.CharField(verbose_name=_('operator'),
                          max_length=2,
                          choices=RADOP_REPLY_TYPES,
                          default='=')
    value = models.CharField(verbose_name=_('value'), max_length=253)

    class Meta:
        db_table = 'radgroupreply'
        verbose_name = _('radiusgroupreply')
        verbose_name_plural = _('radiusgroupreplies')
        abstract = True

    def __str__(self):
        return str(self.group_name)


class AbstractRadiusGroupCheck(TimeStampedEditableModel):
    group_name = models.CharField(verbose_name=_('groupname'),
                                  max_length=64,
                                  db_column='groupname',
                                  db_index=True)
    attribute = models.CharField(verbose_name=_('attribute'), max_length=64)
    op = models.CharField(verbose_name=_('operator'),
                          max_length=2,
                          choices=RADOP_CHECK_TYPES,
                          default=':=')
    value = models.CharField(verbose_name=_('value'), max_length=253)

    class Meta:
        db_table = 'radgroupcheck'
        verbose_name = _('radiusgroupcheck')
        verbose_name_plural = _('radiusgroupcheck')
        abstract = True

    def __str__(self):
        return str(self.group_name)


class AbstractRadiusPostAuthentication(TimeStampedEditableModel):
    user_name = models.CharField(verbose_name=_('username'),
                                 max_length=64,
                                 db_column='username')
    password = models.CharField(verbose_name=_('password'),
                                max_length=64,
                                db_column='pass')
    reply = models.CharField(verbose_name=_('reply'),
                             max_length=32)
    auth_date = models.DateTimeField(verbose_name=_('authdate'),
                                     db_column='authdate',
                                     auto_now=True)

    class Meta:
        db_table = 'radpostauth'
        verbose_name = _('radiuspostauthentication')
        verbose_name_plural = _('radiuspostauthentication')
        abstract = True

    def __str__(self):
        return str(self.user_name)
