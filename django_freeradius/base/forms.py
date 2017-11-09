from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from . models import AbstractRadiusCheck
from .. import settings as app_settings

import re

class AbstractRadiusCheckAdminForm(forms.ModelForm):
    # custom field not backed by database
    new_value = forms.CharField(label=_('new Value'), required=False, 
                                min_length=8, max_length=16,
                                widget=forms.PasswordInput(),
                                help_text=_('must be 8-16 characters '
                                'long and may contain only the following'
                                ' characters:'
                'A-Z, a-z, 0-9, ! % - _ + = [ ] { } : , . ? < > ( ) ; '))

    def clean_attribute(self):
        if self.data['attribute'] not in app_settings.DISABLED_SECRET_FORMAT:
            return self.cleaned_data["attribute"]
        raise ValidationError('This SECRET FORMAT is disabled'
                              ', please use another one')
    def clean_new_value(self):
        # if something else is required to validates your data
        # according to European GDPR
        regexp_lowercase  = r'[a-z]'
        regexp_uppercase = r'[A-Z]'
        regexp_number     = r'[0-9]'
        regexp_special    = r'[\!\%\-_+=\[\]\{\}\:\,\.\?\<\>\(\)\;]'
        regexp2test  = [regexp_lowercase,
                        regexp_uppercase,
                        regexp_number,
                        regexp_special]
        for regexp in regexp2test:
            if not re.findall(regexp, self.data['new_value']):
                raise ValidationError('The secret must contains lowercase'
                                      ' and uppercase characters, '
                                      ' number and at least one of these symbol'
                                      ' ! % - _ + = [ ] { } : , . ? < > ( ) ;'
                                      )
        return self.cleaned_data["new_value"]

    class Meta:
        model = AbstractRadiusCheck
        fields = '__all__'
