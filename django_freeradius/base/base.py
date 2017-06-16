from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import AutoLastModifiedField


class TimeStampedEditableAdmin(models.Model):

    # An abstract base class model that provides self-updating
    # modified  fields.

    id = models.UUIDField(primary_key=True, editable=False)
    modified = AutoLastModifiedField(_('modified'), editable=True)

    class Meta:
        abstract = True
