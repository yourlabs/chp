from django.forms.boundfield import BoundField
from django.forms.fields import Field
from django.utils.functional import Promise
from django.utils.html import conditional_escape, format_html
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
        # cast any lazy translation strings
        if isinstance(contents, Promise):
            contents = conditional_escape(contents)
        return contents

    @staticmethod
    def render(field, widget=None, attrs=None, only_initial=False):
        """Introspect the field and call an MDC render method."""
        if isinstance(field, BoundField):
            widget_type = field.field.widget.__class__.__name__
            mdc_render = getattr(
                Factory, f"mdc_{widget_type.lower()}", None)
            if mdc_render is not None:
                # code from from boundfield.as_widget()
                widget = field.field.widget
                if field.field.localize:
                    widget.is_localized = True
                attrs = attrs or {}
                attrs = field.build_widget_attrs(attrs, widget)
                if field.auto_id and 'id' not in widget.attrs:
                    attrs.setdefault('id',
                                     field.html_initial_id
                                     if only_initial else field.auto_id)
                context = widget.get_context(
                    name=(field.html_initial_name
                          if only_initial else field.html_name),
                    value=field.value(),
                    attrs=attrs
                )
                label = Factory.get_label(field)
                for_id = widget.attrs.get('id') or field.auto_id
                context.update(
                    {'label': label,
                     'for': widget.id_for_label(for_id),
                     'type':
                        context['widget'].get('type',
                                              field.field.widget.input_type),
                     })

                return mdc_render(context)
        raise NotImplementedError

    @staticmethod
    def mdc_checkboxinput(context):
        mdc_type = "checkbox"

        props, children = [], []
        props.append(
            cp("name", context['widget']['name']))
        if context["widget"]["value"] is not None:
            cp("value", context["widget"]["value"])

        for attr, value in context['widget']['attrs'].items():
            props.append(cp(attr, value))

        return mdc.CheckboxField(props, children, context)

    @staticmethod
    def mdc_textinput(context):
        mdc_type = "text"

        props, children = [], []
        props.append(
            cp("name", context['widget']['name']))
        if context["widget"]["value"] is not None:
            props.append(
                cp("value", context["widget"]["value"]))

        for attr, value in context['widget']['attrs'].items():
            props.append(cp(attr, value))

        return mdc.TextField(props, children, context)

    @staticmethod
    def mdc_dateinput(context):
        mdc_type = "date"

        props, children = [], []
        props.append(
            cp("name", context['widget']['name']))
        if context["widget"]["value"] is not None:
            props.append(
                cp("value", context["widget"]["value"]))

        for attr, value in context['widget']['attrs'].items():
            props.append(cp(attr, value))

        return mdc.DateField(props, children, context)

    @staticmethod
    def mdc_select(context):
        mdc_type = "select"
        props, children = [], []
        props.append(
            cp("name", context['widget']['name']))

        for attr, value in context['widget']['attrs'].items():
            props.append(cp(attr, value))

        # Implementation of
        # django/forms/templates/django/forms/widgets/select.html
        for group_name, group_choices, group_index in \
                context["widget"]["optgroups"]:
            props_group, children_group = [], []
            if group_name:
                props_group = [cp("label", group_name)]

            for option in group_choices:
                props_option = []
                option_label = option["label"]
                if option["value"] == "":
                    option_label = ""
                props_option.append(
                    cp("value", str(option["value"])))
                for attr, value in option['attrs'].items():
                    props_option.append(cp(attr, value))
                children_group.append(
                    chp.Option(props_option, option_label))

            if group_name:
                children.append(
                    chp.Optgroup(props_group, children_group))
            else:
                children.extend(children_group)

        return mdc.SelectField(props, children, context)
