
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .widget import *


default_app_config = 'leonardo_module_forms.FormConfig'


class Default(object):

    optgroup = ('Forms')

    @property
    def apps(self):
        INSTALLED_APPS = []
        try:
            import django_remote_forms # noqa
        except ImportError:
            pass
        else:
            INSTALLED_APPS += ['django_remote_forms']

        return INSTALLED_APPS + [
            'crispy_forms',
            'form_designer',
            'leonardo_module_forms',
        ]

    @property
    def widgets(self):
        return [
            FormWidget,
        ]

    config = {
        'FORM_FILES_PRIVATE': (True, 'Makes all uploaded files from forms as private'),
        'FORM_FILES_DIRECTORY': ('form files', 'Upload all form files to this directory'),
    }


class FormConfig(AppConfig):
    name = 'leonardo_module_forms'
    verbose_name = "Module Forms"

    conf = Default()

    def ready(self):

        from form_designer import settings, models
        settings.FORM_DESIGNER_FIELD_TYPES = 'leonardo_module_forms.fields.LEONARDO_FIELD_TYPES'
        from .fields import LEONARDO_FIELD_TYPES
        models.FIELD_TYPES = LEONARDO_FIELD_TYPES

default = Default()
