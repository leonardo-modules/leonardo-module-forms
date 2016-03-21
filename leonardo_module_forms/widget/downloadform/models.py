# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo_module_forms.widget.form.models import FormWidget
from leonardo.module.media.fields import FileField

class DownloadFormWidget(FormWidget):


    file = models.ForeignKey("media.File", 
                             verbose_name=_("file"),
                             related_name="%(app_label)s_%(class)s_files")

    class Meta:
        abstract = True
        verbose_name = _('Download form')
        verbose_name_plural = _('Download forms')

