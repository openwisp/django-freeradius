import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .. import settings as app_settings
from .models import AbstractRadiusCheck


class AbstractRadiusCheckAdminForm(forms.ModelForm):
    _secret_help_text = _('The secret must contains lowercase'
                          ' and uppercase characters, '
                          ' number and at least one of these symbols:'
                          '! % - _ + = [ ] { } : , . ? < > ( ) ; ')
    # custom field not backed by database
    new_value = forms.CharField(label=_('Value'), required=False,
                                min_length=8, max_length=16,
                                widget=forms.PasswordInput(),
                                help_text=_secret_help_text)

    def clean_attribute(self):
        if self.data['attribute'] not in app_settings.DISABLED_SECRET_FORMATS:
            return self.cleaned_data["attribute"]
        # this is not covered anymore
        # raise ValidationError('This SECRET FORMAT is disabled'
        #                      ', please use another one')

    def clean_new_value(self):
        for regexp in app_settings.RADCHECK_SECRET_VALIDATORS.values():
            found = re.findall(regexp, self.data['new_value'])
            if not found:
                raise ValidationError(self._secret_help_text)
        return self.cleaned_data["new_value"]

    class Meta:
        model = AbstractRadiusCheck
        fields = '__all__'
