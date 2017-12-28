from django import forms
from .models import RAD_NAS_TYPES

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
