import swapper
from django.conf import settings


def get_model(apps, model_path):
    app, model = model_path.split('.')
    return apps.get_model(app, model)


def get_swapped_model(apps, app_name, model_name):
    model_path = swapper.get_model_name(app_name, model_name)
    return get_model(apps, model_path)


SESSION_TIME_ATTRIBUTE = 'Max-Daily-Session'
SESSION_TRAFFIC_ATTRIBUTE = 'Max-Daily-Session-Traffic'
DEFAULT_SESSION_TIME_LIMIT = '10800'  # seconds
DEFAULT_SESSION_TRAFFIC_LIMIT = '3000000000'  # bytes (octets)


def add_default_groups(apps, schema_editor):
    RadiusGroup = get_swapped_model(apps, 'django_freeradius', 'RadiusGroup')
    RadiusGroupCheck = get_swapped_model(apps, 'django_freeradius', 'RadiusGroupCheck')
    if not RadiusGroup.objects.exists():
        default = RadiusGroup(name='users',
                              description='Regular users',
                              default=True)
        default.save()
        check = RadiusGroupCheck(group_id=default.id,
                                 groupname=default.name,
                                 attribute=SESSION_TIME_ATTRIBUTE,
                                 op=':=',
                                 value=DEFAULT_SESSION_TIME_LIMIT)
        check.save()
        check = RadiusGroupCheck(group_id=default.id,
                                 groupname=default.name,
                                 attribute=SESSION_TRAFFIC_ATTRIBUTE,
                                 op=':=',
                                 value=DEFAULT_SESSION_TRAFFIC_LIMIT)
        check.save()
        power_users = RadiusGroup(name='power-users',
                                  description='Users with less restrictions',
                                  default=False)
        power_users.save()


def add_default_group_to_existing_users(apps, schema_editor):
    User = get_model(apps, settings.AUTH_USER_MODEL)
    RadiusUserGroup = get_swapped_model(apps, 'django_freeradius', 'RadiusUserGroup')
    RadiusGroup = get_swapped_model(apps, 'django_freeradius', 'RadiusGroup')
    default_group = RadiusGroup.objects.filter(default=True)
    if default_group.exists():
        default_group = default_group.first()
        for user in User.objects.all():
            if not RadiusUserGroup.objects.filter(user=user).exists():
                user_group = RadiusUserGroup(user_id=user.id,
                                             username=user.username,
                                             group_id=default_group.id)
                user_group.save()
