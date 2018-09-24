from django.conf import settings
from django.db import migrations

from . import add_default_groups, add_default_group_to_existing_users


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_freeradius', '0002_add_customizations'),
    ]

    operations = [
        migrations.RunPython(add_default_groups,
                             reverse_code=migrations.RunPython.noop),
        migrations.RunPython(add_default_group_to_existing_users,
                             reverse_code=migrations.RunPython.noop),
    ]
