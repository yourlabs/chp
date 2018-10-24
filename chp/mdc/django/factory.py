from django.forms.boundfield import BoundField
from django.forms.fields import Field
from django.utils.functional import Promise
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

import django.forms.widgets as Widgets

from ... import components as chp
from .. import components as mdc

# alias for chp.pyreact.create_prop()
cp = chp.cp


class Factory:

    @staticmethod
    def get_label(field):
        # code taken from Boundfield.label_tag()
        contents = field.label
        label_suffix = (field.field.label_suffix
                        if field.field.label_suffix is not None
                        else (field.form.label_suffix
                              if hasattr(field, "form") else ""))
        if label_suffix and contents and contents[-1] not in _(':?.!'):
            contents = format_html('{}{}', contents, label_suffix)
        return contents

    @staticmethod
    def render(field):
        """Introspect the field and call an MdcWidget render method."""
        if isinstance(field, BoundField):
            widget_type = field.field.widget.__class__.__name__
            mdc_widget = getattr(
                MdcWidgets, f"Mdc{widget_type}")
            label = Factory.get_label(field)
            return field.as_widget(mdc_widget(label=label))
        raise NotImplementedError


class ChpWidgetMixin:
    chp_widget = None

    def __init__(self, attrs=None, **kwargs):
        """Capture the field label in the widget."""
        self.label = kwargs.pop("label", None)
        if attrs is not None:
            attrs = attrs.copy()
        super().__init__(attrs)

    def _add_label(self, context):
        """Add the field label to the widget context."""
        label = self.label
        # cast any lazy translation strings
        if isinstance(label, Promise):
            label = conditional_escape(label)

        context['widget'].update(
            {'label': label,
             'id_for_label':
                self.id_for_label(context['widget']['attrs']['id'])
             })
        return context

    def get_mdc_context(self, context):
        """Update the context for MDC components."""
        context = self._add_label(context)
        context.update({
            "type": context['widget']['type'],
            "label": context['widget']['label'],
            "for": context['widget']['id_for_label'],
        })
        return context

    def _render(self, template_name, context, renderer=None):
        """Render the widget as a CHP MDC AST."""
        # prepare the field label
        context = self.get_mdc_context(context)
        return self._mdc_render(context)

    def _mdc_render(self, context):
        """Override this method for MDC widget rendering."""
        raise NotImplementedError


class MdcWidgets:
    class MdcCheckboxInput(ChpWidgetMixin, Widgets.CheckboxInput):
        mdc_type = "checkbox"

        def _mdc_render(self, context):
            props, children = [], []
            props.append(
                cp("name", context['widget']['name']))

            for attr, value in context['widget']['attrs'].items():
                props.append(cp(attr, value))

            return mdc.CheckboxField(props, children, context)

    class MdcTextInput(ChpWidgetMixin, Widgets.TextInput):
        mdc_type = "text"

        def _mdc_render(self, context):
            props, children = [], []
            props.append(
                cp("name", context['widget']['name']))

            for attr, value in context['widget']['attrs'].items():
                props.append(cp(attr, value))

            return mdc.TextField(props, children, context)

    class MdcDateInput(ChpWidgetMixin, Widgets.DateInput):
        mdc_type = "date"

        def _mdc_render(self, context):
            props, children = [], []
            props.append(
                cp("name", context['widget']['name']))

            for attr, value in context['widget']['attrs'].items():
                props.append(cp(attr, value))

            return mdc.DateField(props, children, context)

    class MdcSelect(ChpWidgetMixin, Widgets.Select):
        mdc_type = "select"

        def _mdc_render(self, context):
            props, children = [], []
            props.append(
                cp("name", context['widget']['name']))

            for attr, value in context['widget']['attrs'].items():
                props.append(cp(attr, value))

            # TODO: build children list of options from queryset.
            # TODO: create optgroups if required.

            return mdc.SelectField(props, children, context)
