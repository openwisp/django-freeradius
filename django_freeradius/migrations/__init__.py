import swapper
from django.conf import settings


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
