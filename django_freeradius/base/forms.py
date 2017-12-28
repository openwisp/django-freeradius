import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .. import settings as app_settings
from .models import RAD_NAS_TYPES, AbstractRadiusCheck

radcheck_value_field = AbstractRadiusCheck._meta.get_field('value')


class AbstractRadiusCheckAdminForm(forms.ModelForm):
    _secret_help_text = _('The secret must contains lowercase'
                          ' and uppercase characters, '
                          ' number and at least one of these symbols:'
                          '! % - _ + = [ ] { } : , . ? < > ( ) ; ')
    # custom field not backed by database
    new_value = forms.CharField(label=_('Value'), required=False,
                                min_length=8,
                                max_length=radcheck_value_field.max_length,
                                widget=forms.PasswordInput(),
                                help_text=_secret_help_text)

    def clean_attribute(self):
        if self.data['attribute'] not in app_settings.DISABLED_SECRET_FORMATS:
            return self.cleaned_data["attribute"]

    def clean_new_value(self):
        if not self.data['new_value']:
            return None
        for regexp in app_settings.RADCHECK_SECRET_VALIDATORS.values():
            found = re.findall(regexp, self.data['new_value'])
            if not found:
                raise ValidationError(self._secret_help_text)
        return self.cleaned_data["new_value"]

    class Meta:
        model = AbstractRadiusCheck
        fields = '__all__'


# class for add customer fields in the NAS
class NasModelForm(forms.ModelForm):

    standard_type = forms.ChoiceField(choices=RAD_NAS_TYPES,
                                      help_text="choose one of the standard types...",
                                      initial='Other',
                                      )

    other_NAS_type = forms.CharField(help_text="...or write a new type.",
                                     required=False,
                                     max_length=30,
                                     )

    class Meta:
        fields = '__all__'
