from django.conf import settings
from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import swapper
import uuid


def get_model(apps, model_path):
    app, model = model_path.split('.')
    return apps.get_model(app, model)


def get_swapped_model(apps, app_name, model_name):
    model_path = swapper.get_model_name(app_name, model_name)
    return get_model(apps, model_path)


def add_default_profiles(apps, schema_editor):
    RadiusProfile = get_swapped_model(apps, 'django_freeradius', 'RadiusProfile')
    default_profile = RadiusProfile.objects.filter(default=True)
    if not default_profile.exists():
        limited_user = RadiusProfile(name="Limited User", default=True,
                                     daily_session_limit=10800,
                                     daily_bandwidth_limit=3000000000)
        limited_user.save()
        power_user = RadiusProfile(name="Power User",
                                   daily_session_limit=172800,
                                   daily_bandwidth_limit=100000000000)
        power_user.save()


def add_default_profile_to_existing_users(apps, schema_editor):
    User = get_model(apps, settings.AUTH_USER_MODEL)
    RadiusUserProfile = get_swapped_model(apps, 'django_freeradius', 'RadiusUserProfile')
    RadiusProfile = get_swapped_model(apps, 'django_freeradius', 'RadiusProfile')
    default_profile = RadiusProfile.objects.filter(default=True)
    if default_profile.exists():
        users = User.objects.all()
        for user in users:
            if not RadiusUserProfile.objects.filter(user=user).exists():
                user_profile = RadiusUserProfile(user=user, profile=default_profile[0])
                user_profile.save()


class Migration(migrations.Migration):
    replaces = [
        ('django_freeradius', '0015_radiusbatch'),
        ('django_freeradius', '0016_radiusprofile'),
        ('django_freeradius', '0017_radiususerprofile'),
        ('django_freeradius', '0018_add_default_profile'),
        ('django_freeradius', '0019_auto_20180705_1745'),
        ('django_freeradius', '0020_auto_20180708_1237'),
        ('django_freeradius', '0021_auto_20180709_2139'),
        ('django_freeradius', '0022_auto_20180713_1713')
    ]
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_freeradius', '__first__'),
        ('django_freeradius', '0014_auto_20171226_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='radiuscheck',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='radiuscheck',
            name='valid_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='radiuscheck',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='radiusaccounting',
            name='called_station_id',
            field=models.CharField(blank=True, db_column='calledstationid', db_index=True, max_length=50, null=True, verbose_name='called station ID'),
        ),
        migrations.AlterField(
            model_name='radiusaccounting',
            name='calling_station_id',
            field=models.CharField(blank=True, db_column='callingstationid', db_index=True, max_length=50, null=True, verbose_name='calling station ID'),
        ),
        migrations.CreateModel(
            name='RadiusBatch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(db_index=True, help_text='A unique batch name', max_length=128, verbose_name='name')),
                ('strategy', models.CharField(choices=[('prefix', 'Generate from prefix'), ('csv', 'Import from CSV')], db_index=True, help_text='Import users from a CSV or generate using a prefix', max_length=16, verbose_name='strategy')),
                ('csvfile', models.FileField(blank=True, help_text='The csv file containing the user details to be uploaded', null=True, upload_to='', verbose_name='CSV')),
                ('prefix', models.CharField(blank=True, help_text='Usernames generated will be of the format [prefix][number]', max_length=20, null=True, verbose_name='prefix')),
                ('pdf', models.FileField(blank=True, help_text='The pdf file containing list of usernames and passwords', null=True, upload_to='', verbose_name='PDF')),
                ('expiration_date', models.DateField(blank=True, help_text='If left blank users will never expire', null=True, verbose_name='expiration date')),
                ('users', models.ManyToManyField(blank=True, help_text='List of users uploaded in this batch', related_name='radius_batch', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'batch user creation',
                'verbose_name_plural': 'batch user creation operations',
                'db_table': 'radbatch',
                'abstract': False,
                'swappable': 'DJANGO_FREERADIUS_RADIUSBATCH_MODEL',
            },
        ),
        migrations.CreateModel(
            name='RadiusProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(db_index=True, help_text='A unique profile name', max_length=128, verbose_name='name')),
                ('daily_session_limit', models.BigIntegerField(blank=True, null=True, verbose_name='daily session limit')),
                ('daily_bandwidth_limit', models.BigIntegerField(blank=True, null=True, verbose_name='daily bandwidth limit')),
                ('max_all_time_limit', models.BigIntegerField(blank=True, null=True, verbose_name='maximum all time session limit')),
                ('default', models.BooleanField(default=False, verbose_name='Use this profile as the default profile')),
            ],
            options={
                'verbose_name': 'limit profile',
                'verbose_name_plural': 'limit profiles',
                'abstract': False,
                'swappable': 'DJANGO_FREERADIUS_RADIUSPROFILE_MODEL',
            },
        ),
        migrations.CreateModel(
            name='RadiusUserProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.DJANGO_FREERADIUS_RADIUSPROFILE_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='radius_user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user profile',
                'verbose_name_plural': 'user profiles',
                'db_table': 'radiususerprofile',
                'abstract': False,
                'swappable': 'DJANGO_FREERADIUS_RADIUSUSERPROFILE_MODEL',
            },
        ),
        migrations.RunPython(add_default_profiles, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(add_default_profile_to_existing_users, reverse_code=migrations.RunPython.noop),
    ]
