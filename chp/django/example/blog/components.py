from django.forms.boundfield import BoundField
from django.forms.widgets import Widget, TextInput, CheckboxInput
from django.utils.functional import Promise
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from chp.components import *
from chp.store import (create_store, render_app)
from chp.mdc.components import *


"""
Boundfield has the following methods to render an HTML widget
using the template engine:
    def __str__(self):
        """ """Render this field as an HTML widget.""" """
        if self.field.show_hidden_initial:
            return self.as_widget() + self.as_hidden(only_initial=True)
        return self.as_widget()

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        """ """
        Render the field by rendering the passed widget, adding any HTML
        attributes passed as attrs. If a widget isn't specified, use the
        field's default widget.
        """ """
        widget = widget or self.field.widget
        if self.field.localize:
            widget.is_localized = True
        attrs = attrs or {}
        attrs = self.build_widget_attrs(attrs, widget)
        if self.auto_id and 'id' not in widget.attrs:
            attrs.setdefault('id', self.html_initial_id if only_initial else self.auto_id)
        return widget.render(
            name=self.html_initial_name if only_initial else self.html_name,
            value=self.value(),
            attrs=attrs,
            renderer=self.form.renderer,
        )

    def build_widget_attrs(self, attrs, widget=None):
        widget = widget or self.field.widget
        attrs = dict(attrs)  # Copy attrs to avoid modifying the argument.
        if widget.use_required_attribute(self.initial) and self.field.required and self.form.use_required_attribute:
            attrs['required'] = True
        if self.field.disabled:
            attrs['disabled'] = True
        return attrs

We need to use similar to get the attrs for 'required', etc.

Alternatively, create custom MdcWidgets and override the widget.render()?

Refactor functions here to classes to support code reuse.
"""


class ChpWidgetMixin:
    chp_widget = None

    def __init__(self, attrs=None, **kwargs):
        self.label = kwargs.pop("label", None)
        if attrs is not None:
            attrs = attrs.copy()
        super().__init__(attrs)

    def _add_label(self, context):
        context['widget'].update(
            {'label': self.label,
             'id_for_label':
                self.id_for_label(context['widget']['attrs']['id'])
             })
        return context

    def _render(self, template_name, context, renderer=None):
        '''Ignore template_name and renderer (see django.forms.py)
        '''
        context = self._add_label(context)
        raise NotImplementedError


class MdcCheckboxInput(ChpWidgetMixin, CheckboxInput):

    def _render(self, template_name, context, renderer=None):
        context = self._add_label(context)

        props, children = [], []
        props.append(
            cp("type", "checkbox"),
            )
        checked = context['widget']['attrs'].get('checked', False)
        if checked:
            props.append(cp("checked", checked))
        el_id = context['widget']['attrs'].get('id', None)
        if el_id:
            props.append(cp("id", el_id))

        label = context['widget']['label']
        if isinstance(label, Promise):
            label = conditional_escape(label)
        context.update({
            "label": label,
            "for": context['widget']['id_for_label'],
            "type": context['widget']['type'],
        })
        return CheckboxField(props, children, context)


def MdcCheckbox(field):
    # code taken from Boundfield.label_tag()
    label_suffix = (field.field.label_suffix
                    if field.field.label_suffix is not None
                    else (field.form.label_suffix
                          if hasattr(field, "form") else ""))
    contents = field.label
    if label_suffix and contents and contents[-1] not in _(':?.!'):
        label = format_html('{}{}', contents, label_suffix)

    return field.as_widget(MdcCheckboxInput(label=label))


def MdcInput(field):
    # typ = field.field.widget.input_type
    typ = field.mdc_type
    # widget formatted value
    value = field.field.widget.format_value(field.value())

    props = [
        cp("type", typ),
        ]
    if value:
        props.append(cp("value", value))
    if field.auto_id:
        props.append(cp("id", field.auto_id))

    # widget-level attrs
    for (key, value) in field.field.widget.attrs.items():
        props.append(
            cp(key, value)
        )
    return Input(props, [])


def DjLabel(field):
    label = field.label
    # cast gettext_lazy strings so they are recognised by AST renderer
    if isinstance(label, Promise):
        label = conditional_escape(label)

    props = [
        cp("for", field.id_for_label),
    ]
    context = {
        "type": field.mdc_type,
        "for": field.id_for_label,
        "label": label,
    }

    return Label(props, label, context)


def MdcTextField(field):
    # to differentiate from Django date field
    if not hasattr(field, "mdc_type"):
        field.mdc_type = "text"
    props = [
        cp("type", field.mdc_type),
        ]
    children = [
        MdcInput(field),
        DjLabel(field),
        LineRipple(),
    ]
    return InputField(props, children)


def MdcDateField(field):
    field.mdc_type = "date"
    return MdcTextField(field)
