import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .. import settings as app_settings
from .models import AbstractRadiusCheck


class AbstractRadiusCheckAdminForm(forms.ModelForm):
    # custom field not backed by database
    new_value = forms.CharField(label=_('new Value'), required=False,
                                min_length=8, max_length=16,
                                widget=forms.PasswordInput(),
                                help_text=_(
                                'must be 8-16 characters '
                                'long and may contain only the following '
                                'characters: '
                                'A-Z, a-z, 0-9, '
                                '! % - _ + = [ ] { } : , . ? < > ( ) ; ')
                                )

    def clean_attribute(self):
        if self.data['attribute'] not in app_settings.DISABLED_SECRET_FORMAT:
            return self.cleaned_data["attribute"]
        raise ValidationError('This SECRET FORMAT is disabled'
                              ', please use another one')

    def clean_new_value(self):
        for regexp in app_settings.RADCHECK_SECRET_VALIDATORS.values():
            found = re.findall(regexp, self.data['new_value'])
            if not found:
                raise ValidationError('The secret must contains lowercase'
                                      ' and uppercase characters, '
                                      ' number and at least one of these symbols:'
                                      ' ! % - _ + = [ ] { } : , . ? < > ( ) ;'
                                      )
        return self.cleaned_data["new_value"]

    class Meta:
        model = AbstractRadiusCheck
        fields = '__all__'
