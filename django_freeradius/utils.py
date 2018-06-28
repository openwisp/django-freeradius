import csv
from io import StringIO

import swapper
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import validate_email
from django.template.loader import get_template
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from xhtml2pdf import pisa

from django_freeradius.settings import BATCH_PDF_TEMPLATE


def find_available_username(username, users_list, prefix=False):
    User = get_user_model()
    suffix = 1
    tmp = '{}{}'.format(username, suffix) if prefix else username
    names_list = map(lambda x: x.username, users_list)
    while User.objects.filter(username=tmp).exists() or tmp in names_list:
        suffix += 1 if prefix else 0
        tmp = '{}{}'.format(username, suffix)
        suffix += 1 if not prefix else 0
    return tmp


def validate_csvfile(csvfile):
    csv_data = csvfile.read()
    csv_data = csv_data.decode('utf-8') if isinstance(csv_data, bytes) else csv_data
    reader = csv.reader(StringIO(csv_data), delimiter=',')
    error_message = "The CSV contains a line with invalid data,\
                    line number {} triggered the following error: {}"
    row_count = 1
    for row in reader:
        if len(row) == 5:
            username, password, email, firstname, lastname = row
            try:
                validate_email(email)
            except ValidationError as e:
                raise ValidationError(_(error_message.format(str(row_count), e.message)))
            row_count += 1
        elif len(row) > 0:
            raise ValidationError(_(error_message.format(str(row_count), "Improper CSV format.")))
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
    html = template.render(data)
    f = open('{}.pdf'.format(prefix), 'w+b')
    pisa.CreatePDF(html.encode('utf-8'), dest=f, encoding='utf-8')
    f.seek(0)
    return File(f)


def set_default_limits(sender, instance, created, **kwargs):
    if created:
        radprofile = swapper.load_model('django_freeradius', 'RadiusProfile')
        raduserprofile = swapper.load_model('django_freeradius', 'RadiusUserProfile')
        default_profile = radprofile.objects.filter(default=True)
        if default_profile.exists():
            userprofile = raduserprofile(profile=default_profile[0], user=instance)
            userprofile.save()
