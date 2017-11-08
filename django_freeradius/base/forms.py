from django import forms
from django.utils.translation import ugettext_lazy as _

from . models import AbstractRadiusCheck

class AbstractRadiusCheckAdminForm(forms.ModelForm):
    # custom field not backed by database
    new_value = forms.CharField(label=_('new value'), required=False, 
                                widget=forms.PasswordInput(),
                                help_text=_('Renew the password value'))

    class Meta:
        model = AbstractRadiusCheck
        fields = '__all__'
