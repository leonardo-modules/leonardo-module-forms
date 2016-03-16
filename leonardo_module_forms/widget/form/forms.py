# -#- coding: utf-8 -#-

from crispy_forms.bootstrap import *
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.layout import HTML, Field, Fieldset, Layout
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from form_designer.models import Form, FormField
from horizon_contrib.forms import SelfHandlingModelForm
from leonardo.forms.fields.dynamic import DynamicModelChoiceField
import copy
from leonardo.module.web.widgets.forms import WidgetUpdateForm
from .tables import FormFieldsFormset


class FormForm(SelfHandlingModelForm):

    def __init__(self, *args, **kwargs):
        super(FormForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            TabHolder(

                Tab(_('Base'),
                    'title', 'config_json'
                    ),
            )
        )

        if 'request' in kwargs:
            _request = copy.copy(kwargs['request'])
            _request.POST = {}
            _request.method = 'GET'
            from .tables import FormFieldsTable

            try:
                form = self._meta.model.objects.get(
                    id=kwargs['initial']['id'])
            except:
                form = None
                data = []
            else:
                data = form.fields

            dimensions = Tab(_('Fields'),
                             HTML(
                                 FormFieldsTable(_request,
                                                 form=form,
                                                 data=data).render()),
                             )
            self.helper.layout[0].append(dimensions)

    def handle_related_models(self, request, obj):
        """Handle related models
        """
        formset = FormFieldsFormset(
            request.POST, prefix='fields')
        for form in formset.forms:
            if form.is_valid():
                if 'id' in form.cleaned_data:
                    form.save()
            else:
                # little ugly
                data = form.cleaned_data
                data['form'] = obj
                data.pop('DELETE', None)
                wd = FormField(**data)
                wd.save()
        # optionaly delete dimensions
        if formset.is_valid():
            formset.save(commit=False)
            # delete objects
            for obj in formset.deleted_objects:
                obj.delete()
        return True

    class Meta:
        model = Form
        exclude = tuple()


class FormWidgetForm(WidgetUpdateForm):

    form = DynamicModelChoiceField(
        label=_("Form"),
        help_text=_("Select form."),
        queryset=Form.objects.all(),
        search_fields=[
            'title__icontains',
        ],
        add_item_link=reverse_lazy('forms:create_with_form',
                                   kwargs={'cls_name': 'form_designer.form',
                                           'form_cls': 'leonardo_module_forms.widget.form.forms.FormForm'}))
