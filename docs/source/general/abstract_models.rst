===============
Abstract Models
===============

Firstly, need to add basic models TimeStampedEditableModel is an abstract base class model, that provides self-updating
created and modified fields. Write  base class and put abstract=True in the Meta class. This model will then not be used to
create any database table. Instead, when it is used as a base class for other models, it's fields will be added to those
of the child class.

Example of TimeStampedEditableModel code:

.. code-block:: python

   #django_freeradius/base/models.py

   from model_utils.fields import AutoCreatedField, AutoLastModifiedField

   class TimeStampedEditableModel(models.Model):
       """
       An abstract base class model that provides self-updating
       ``created`` and ``modified`` fields.
       """
       created = AutoCreatedField(_('created'), editable=True)
       modified = AutoLastModifiedField(_('modified'), editable=True)

       class Meta:
           abstract = True


Include the TimeStampedEditableModel to the AbstractModel
---------------------------------------------------------
Example:

.. code-block:: python

   #django_freeradius/base/models.py

    class BaseModel(TimeStampedEditableModel):
        id = None

    class Meta:
        abstract = True


    class AbstractRadiusReply(BaseModel):
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


Introduce a ModelAdmin for TimeStampedEditableAdmin
---------------------------------------------------

Example of code:

.. code-block:: python


   #django_freeradius/base/admin.py

   from django.contrib.admin import ModelAdmin
   from openwisp_utils.admin import TimeReadonlyAdminMixin

   class TimeStampedEditableAdmin(TimeReadonlyAdminMixin, ModelAdmin):
        pass


   class AbstractRadiusReplyAdmin(TimeStampedEditableAdmin):
        pass


Creating a Reusable App
-----------------------

First, You have to install `swapper`.  If you are publishing your reusable app as a Python package,
be sure to add `swapper` to your project's dependencies.You may also want to take a look at the `Swapper Guide
<https://github.com/wq/django-swappable-models>`

Install swapper:

.. code-block:: shell

   pip install swapper


In your reusable models use import swapper  and  add to Meta class  swappable = swapper.swappable_setting('reusable_app', 'model'):

.. code-block:: python

   #django_freeradius/models.py

   import swapper

   from .base.models import (AbstractNas, AbstractRadiusAccounting,
                             AbstractRadiusCheck, AbstractRadiusGroupCheck,
                             AbstractRadiusGroupReply, AbstractRadiusPostAuth,
                             AbstractRadiusReply, AbstractRadiusUserGroup)


    class RadiusCheck(AbstractRadiusCheck):
        class Meta(AbstractRadiusCheck.Meta):
            abstract = False
            swappable = swappable_setting('django_freeradius', 'RadiusCheck')


Migrations
----------

Swapper can also be used in Django 1.7+ migration scripts to facilitate dependency ordering and
foreign key references. To use this feature in your library, generate a migration script with makemigrations
and make the following changes:

.. code-block:: python

   #django_freeradius/migrations

   import swapper

   class Migration(migrations.Migration):

       initial = True

    dependencies = [
        swapper.dependency('django_freeradius', 'RadiusReply'),
        swapper.dependency('django_freeradius', 'RadiusCheck'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('nas_name', models.CharField(db_column='nasname', db_index=True, help_text='NAS Name (or IP address)', max_length=128, unique=True, verbose_name='nas name')),
                ('short_name', models.CharField(db_column='shortname', max_length=32, verbose_name='short name')),
                ('type', models.CharField(max_length=30, verbose_name='type')),
                ('secret', models.CharField(help_text='Shared Secret', max_length=60, verbose_name='secret')),
                ('ports', models.IntegerField(blank=True, null=True, verbose_name='ports')),
                ('community', models.CharField(blank=True, max_length=50, null=True, verbose_name='community')),
                ('description', models.CharField(max_length=200, null=True, verbose_name='description')),
                ('server', models.CharField(max_length=64, null=True, verbose_name='server')),
            ],
            options={
                'db_table': 'nas',
                'swappable': swapper.swappable_setting('django_freeradius', 'Nas'),
                'verbose_name': 'nas',
                'abstract': False,
                'verbose_name_plural': 'nas',
            },
        ),

Extends Models
--------------

The user of your app can override one or both models in their own app.

Example:

.. code-block:: python

   #sample_radius/models.py

   from django.db import models
   from django.utils.translation import ugettext_lazy as _

   from django_freeradius.models import (AbstractNas, AbstractRadiusAccounting,
                                         AbstractRadiusCheck,
                                         AbstractRadiusGroupCheck, AbstractRadiusGroupReply,
                                         AbstractRadiusPostAuth,
                                         AbstractRadiusReply, AbstractRadiusUserGroup)


   class RadiusCheck(AbstractRadiusCheck):
       details = models.CharField(
               verbose_name=_('details'), max_length=64, blank=True, null=True)


Add swapper.load_model() to sample_radius/admin.py. Example:

.. code-block:: python

   from django.contrib import admin

   import swapper
   from django_freeradius.admin import (AbstractNasAdmin,
                                        AbstractRadiusAccountingAdmin,
                                        AbstractRadiusCheckAdmin,
                                        AbstractRadiusGroupCheckAdmin,
                                        AbstractRadiusGroupReplyAdmin,
                                        AbstractRadiusPostAuthAdmin,
                                        AbstractRadiusReplyAdmin,
                                        AbstractRadiusUserGroupAdmin)

   RadiusGroupReply = swapper.load_model("django_freeradius", "RadiusGroupReply")
   RadiusGroupCheck = swapper.load_model("django_freeradius", "RadiusGroupCheck")
   RadiusUserGroup = swapper.load_model("django_freeradius", "RadiusUserGroup")
   RadiusReply = swapper.load_model("django_freeradius", "RadiusReply")
   RadiusCheck = swapper.load_model("django_freeradius", "RadiusCheck")
   RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
   Nas = swapper.load_model("django_freeradius", "Nas")
   RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")


   @admin.register(RadiusCheck)
   class RadiusCheckAdmin(AbstractRadiusCheckAdmin):
       pass


---------------
Update Settings
---------------

Update the settings to trigger the swapper:

.. code-block:: python

   #django_freeradius/tests/settings.py

   if os.environ.get('SAMPLE_APP', False):
           INSTALLED_APPS.append('sample_radius')
           DJANGO_FREERADIUS_RADIUSREPLY_MODEL = "sample_radius.RadiusReply"
           DJANGO_FREERADIUS_RADIUSGROUPREPLY_MODEL = "sample_radius.RadiusGroupReply"
           DJANGO_FREERADIUS_RADIUSCHECK_MODEL = "sample_radius.RadiusCheck"
           DJANGO_FREERADIUS_RADIUSGROUPCHECK_MODEL = "sample_radius.RadiusGroupCheck"
           DJANGO_FREERADIUS_RADIUSACCOUNTING_MODEL = "sample_radius.RadiusAccounting"
           DJANGO_FREERADIUS_NAS_MODEL = "sample_radius.Nas"
           DJANGO_FREERADIUS_RADIUSUSERGROUP_MODEL = "sample_radius.RadiusUserGroup"
           DJANGO_FREERADIUS_RADIUSPOSTAUTHENTICATION_MODEL = "sample_radius.RadiusPostAuth"
