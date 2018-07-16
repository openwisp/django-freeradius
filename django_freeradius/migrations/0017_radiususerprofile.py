# Generated by Django 2.0.5 on 2018-07-01 21:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.DJANGO_FREERADIUS_RADIUSPROFILE_MODEL),
        ('django_freeradius', '0016_radiusprofile'),
    ]

    operations = [
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
                'verbose_name': 'radius user profile',
                'verbose_name_plural': 'radius user profiles',
                'db_table': 'radiususerprofile',
                'abstract': False,
                'swappable': 'DJANGO_FREERADIUS_RADIUSUSERPROFILE_MODEL',
            },
        ),
    ]
