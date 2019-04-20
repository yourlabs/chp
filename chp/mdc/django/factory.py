# import django.forms.widgets as Widgets

from django.forms.boundfield import BoundField
# from django.forms.fields import Field
from django.utils.functional import Promise
from django.utils.html import conditional_escape, format_html
from django.utils.translation import gettext_lazy as _

from ... import components as chp
from .. import components as mdc

# alias for chp.pyreact.create_prop()
cp = chp.cp


class Factory:

    @staticmethod
    def get_label(field):
        """Return a field label with suffix."""
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
        """Introspect the field and call an MDC render method.

        Prepare the widget attrs, field label and context first.
        """
        if not isinstance(field, BoundField):
            raise NotImplementedError

        widget_type = field.field.widget.__class__.__name__
        mdc_render = getattr(
            Factory, f"mdc_{widget_type.lower()}", None)
        if mdc_render is None:
            raise NotImplementedError

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
             'errors': getattr(field, "errors", None),
             })

        return mdc_render(context)

    @staticmethod
    def non_field_errors(form):
        errs = form.errors.get("__all__", form.error_class())
        if errs == []:
            return {}
        props = []
        props.extend([
            cp("class", "errorlist nonfield"),
            ])
        return mdc.ValidationText(props, [],
                                  {"errors": errs, })
        # error_msg = "<br />".join(errs)
        # return chp.Para(props, error_msg)

    @staticmethod
    def errors(field):
        """Render a field validation message."""
        errs = field.form.errors.get(field.name, field.form.error_class())

        if errs == []:
            return {}
        return mdc.ValidationText([], [],
                                  {"name": field.name,
                                   "errors": errs, })

    @staticmethod
    def help_text(field):
        """Render a field help_text."""
        # MDC design: don't show help if there is an error to display.
        errs = field.form.errors.get(field.name, field.form.error_class())
        if errs:
            return {}

        help_text = field.help_text
        if help_text == "":
            return {}
        # cast any lazy translation strings
        if isinstance(help_text, Promise):
            help_text = conditional_escape(help_text)

        return mdc.HelperText([], help_text,
                              {"name": field.name})

    @staticmethod
    def mdc_checkboxinput(context):
        """Render a BooleanField/CheckBoxInput field/widget."""
        # mdc_type = "checkbox"

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
        """Render a CharField/TextInput field/widget."""
        # mdc_type = "text"

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
        """Render a DateField/DateInput field/widget."""
        # mdc_type = "date"

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
        """Render a CharField/choices or ForeignKey/Select field/widget.
        """
        # mdc_type = "select"
        props, children = [], []
        props.append(
            cp("name", context['widget']['name']))

        for attr, value in context['widget']['attrs'].items():
            props.append(cp(attr, value))

        # Implementation of
        # django/forms/templates/django/forms/widgets/select.html
        for group_name, group_choices, _ in \
                context["widget"]["optgroups"]:
            props_group, children_group = [], []
            if group_name:
                props_group = [cp("label", group_name)]

            for option in group_choices:
                props_option = []
                option_label = option["label"]
                # override any 'empty_label' as MDC floating label will be
                # displayed instead.
                if option["value"] == "":
                    option_label = ""
                props_option.append(
                    cp("value", str(option["value"])))
                for attr, value in option['attrs'].items():
                    props_option.append(cp(attr, value))
                children_group.append(
                    chp.Option(props_option, option_label))

            # build list of optgroups
            if group_name:
                children.append(
                    chp.Optgroup(props_group, children_group))
            # or simple list of options
            else:
                children.extend(children_group)

        return mdc.SelectField(props, children, context)
