import swapper

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import migrations

def add_default_profiles(apps, schema_editor):
    RadiusProfile = swapper.load_model('django_freeradius', 'RadiusProfile')
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
    User = get_user_model()
    RadiusUserProfile = swapper.load_model('django_freeradius', 'RadiusUserProfile')
    RadiusProfile = swapper.load_model('django_freeradius', 'RadiusProfile')
    default_profile = RadiusProfile.objects.filter(default=True)
    if default_profile.exists():
        users = User.objects.all()
        for user in users:
            if not RadiusUserProfile.objects.filter(user=user).exists():
                user_profile = RadiusUserProfile(user=user, profile=default_profile[0])
                user_profile.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.DJANGO_FREERADIUS_RADIUSPROFILE_MODEL),
        migrations.swappable_dependency(settings.DJANGO_FREERADIUS_RADIUSUSERPROFILE_MODEL),
        ('django_freeradius', '0017_radiususerprofile'),
    ]

    operations = [
        migrations.RunPython(add_default_profiles, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(add_default_profile_to_existing_users, reverse_code=migrations.RunPython.noop),
    ]
