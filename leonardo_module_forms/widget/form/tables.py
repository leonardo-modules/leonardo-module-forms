
import floppyforms as forms
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon.tables.formset import FormsetDataTable, FormsetRow
from form_designer.models import FormField


class FormFieldsForm(forms.ModelForm):

    class Meta:
        model = FormField
        exclude = tuple()

FormFieldsFormset = modelformset_factory(
    FormField, form=FormFieldsForm, can_delete=True, extra=1)


class CustomFormsetRow(FormsetRow):

    def __init__(self, column, datum, form):
        self.form = form
        super(CustomFormsetRow, self).__init__(column, datum, form)
        # add initial
        if not datum and column.data:
            try:
                previous = column.data[0]
                self.form.fields['id'].initial = previous.id + 1
            except Exception:
                pass


class FormFieldsTable(FormsetDataTable):

    formset_class = FormFieldsFormset

    def get_formset(self):
        """Provide the formset corresponding to this DataTable.

        Use this to validate the formset and to get the submitted data back.
        """
        if self.form:
            queryset = self.form.fields
        else:
            queryset = FormField.objects.none()
        if self._formset is None:
            self._formset = self.formset_class(
                self.request.POST or None,
                initial=self._get_formset_data(),
                prefix=self._meta.name,
                queryset=queryset)
        return self._formset

    def __init__(self, *args, **kwargs):
        self._meta.row_class = CustomFormsetRow
        self.form = kwargs.pop('form', None)
        super(FormFieldsTable, self).__init__(*args, **kwargs)

    form = tables.Column('form', hidden=True)
    name = tables.Column('name')
    title = tables.Column('title')
    type = tables.Column('type', verbose_name=_('Type'))

    name = 'fields'

    class Meta:
        name = 'fields'
        table_name = 'Form Fields'
