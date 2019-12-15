import csv
from io import StringIO

import swapper
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import validate_email
from django.template.loader import get_template
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from weasyprint import HTML

from django_freeradius.settings import BATCH_PDF_TEMPLATE


def find_available_username(username, users_list, prefix=False):
    User = get_user_model()
    suffix = 1
    tmp = "{}{}".format(username, suffix) if prefix else username
    names_list = map(lambda x: x.username, users_list)
    while User.objects.filter(username=tmp).exists() or tmp in names_list:
        suffix += 1 if prefix else 0
        tmp = "{}{}".format(username, suffix)
        suffix += 1 if not prefix else 0
    return tmp


def validate_csvfile(csvfile):
    csv_data = csvfile.read()
    try:
        csv_data = csv_data.decode("utf-8") if isinstance(csv_data, bytes) else csv_data
    except UnicodeDecodeError:
        raise ValidationError(
            _("Unrecognized file format, the supplied file does not look like a CSV file.")
        )
    reader = csv.reader(StringIO(csv_data), delimiter=",")
    error_message = "The CSV contains a line with invalid data,\
                    line number {} triggered the following error: {}"
    row_count = 1
    for row in reader:
        if len(row) == 5:
            username, password, email, firstname, lastname = row
            try:
                validate_email(email)
            except ValidationError as e:
                raise ValidationError(
                    _(error_message.format(str(row_count), e.message))
                )
            row_count += 1
        elif len(row) > 0:
            raise ValidationError(
                _(error_message.format(str(row_count), "Improper CSV format."))
            )
    csvfile.seek(0)


def prefix_generate_users(prefix, n, password_length):
    users_list = []
    user_password = []
    User = get_user_model()
    for i in range(n):
        username = find_available_username(prefix, users_list, True)
        password = get_random_string(length=password_length)
        u = User(username=username)
        u.set_password(password)
        users_list.append(u)
        user_password.append([username, password])
    return users_list, user_password


def generate_pdf(prefix, data):
    template = get_template(BATCH_PDF_TEMPLATE)
    html = HTML(string=template.render(data))
    f = open("{}/{}.pdf".format(settings.MEDIA_ROOT, prefix), "w+b")
    html.write_pdf(target=f)
    f.seek(0)
    return File(f)


def set_default_group(sender, instance, created, **kwargs):
    if created:
        RadiusGroup = swapper.load_model("django_freeradius", "RadiusGroup")
        RadiusUserGroup = swapper.load_model("django_freeradius", "RadiusUserGroup")
        queryset = RadiusGroup.objects.filter(default=True)
        if queryset.exists():
            ug = RadiusUserGroup(user=instance, group=queryset.first())
            ug.full_clean()
            ug.save()


def update_user_related_records(sender, instance, created, **kwargs):
    if created:
        return
    instance.radiususergroup_set.update(username=instance.username)
    instance.radiuscheck_set.update(username=instance.username)
    instance.radiusreply_set.update(username=instance.username)
