from django import forms
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from form_designer.default_field_types import FIELD_TYPES

LEONARDO_FIELD_TYPES = FIELD_TYPES

LEONARDO_FIELD_TYPES.append((
    'file',
    _('File'),
    curry(
        forms.FileField,
    ),
))
LEONARDO_FIELD_TYPES.append((
    'image',
    _('Image'),
    curry(
        forms.ImageField,
    ),
))
