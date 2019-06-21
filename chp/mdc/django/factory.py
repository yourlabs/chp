from django.forms.boundfield import BoundField
from django.utils.functional import Promise
from django.utils.html import conditional_escape, format_html
from django.utils.translation import gettext_lazy as _

from ... import components as chp
from .. import components as mdc

# Alias for chp.pyreact.create_prop().
cp = chp.cp


class Factory:
    """ Provide adapter methods to render Django fields and attributes using
    MDC components rather than a templating engine.
    """

    @staticmethod
    def get_label(field):
        """Return a field label with suffix.

        Code adapted from ~django.forms.Boundfield.label_tag().

        :param ~django.forms.BoundField field: The field being rendered.
        :return: Field label (html_safe).
        :rtype: str
        """
        # Code adapted from ~django.forms.Boundfield.label_tag().
        contents = field.label
        label_suffix = (field.field.label_suffix
                        if field.field.label_suffix is not None
                        else (field.form.label_suffix
                              if hasattr(field, "form") else ""))
        if label_suffix and contents and contents[-1] not in _(':?.!'):
            contents = format_html('{}{}', contents, label_suffix)
        # Cast any lazy translation strings.
        if isinstance(contents, Promise):
            contents = conditional_escape(contents)
        return contents

    @staticmethod
    def render(field, widget=None, attrs=None, only_initial=False):
        """Introspect the field and call an MDC render method to return an AST.

        Prepare the widget attrs, field label and context then render the
        field using MDC components.
        Code adapted from ~django.forms.BoundField.as_widget().

        :param ~django.forms.BoundField field: The field being rendered.
        :param widget: A widget to override the default for the field.
        :type widget: ~django.forms.Widget or None
        :param attrs: Optional widget attributes.
        :type attrs: dict or None
        :param bool only_initial: A flag to render only initial dynamic values.
        :return: An AST representing the rendered field.
        :rtype: list
        """
        if not isinstance(field, BoundField):
            raise NotImplementedError

        widget_type = field.field.widget.__class__.__name__
        mdc_render = getattr(
            Factory, f"mdc_{widget_type.lower()}", None)
        if mdc_render is None:
            raise NotImplementedError

        # Code adapted from ~django.forms.BoundField.as_widget().
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
        """Return an AST of any errors for the form using MDC components.

        :param `~django.forms.Form` form: The form being rendered.
        """
        errs = form.errors.get("__all__", form.error_class())
        if errs == []:
            return {}
        props = []
        props.extend([
            cp("class", "errorlist nonfield"),
            ])
        return mdc.ValidationText(props, [],
                                  {"errors": errs, })

    @staticmethod
    def errors(field):
        """Return an AST of any errors for the field using MDC components.

        :param ~django.forms.BoundField field: The field being rendered.
        """
        errs = field.form.errors.get(field.name, field.form.error_class())

        if errs == []:
            return {}
        return mdc.ValidationText([], [],
                                  {"name": field.name,
                                   "errors": errs, })

    @staticmethod
    def help_text(field):
        """Return an AST of the help_text for the field using MDC components.

        :param ~django.forms.BoundField field: The field being rendered.
        """
        # MDC: don't show help text if there is an error to display.
        errs = field.form.errors.get(field.name, field.form.error_class())
        if errs:
            return {}

        help_text = field.help_text
        if help_text == "":
            return {}
        # Cast any lazy translation strings.
        if isinstance(help_text, Promise):
            help_text = conditional_escape(help_text)

        return mdc.HelperText([], help_text,
                              {"name": field.name})

    @staticmethod
    def mdc_checkboxinput(context):
        """Return an AST for a BooleanField/CheckBoxInput field/widget
        using MDC components.

        :param dict context: Additional widget attributes.
        """

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
        """Return an AST for a CharField/TextInput field/widget using
        MDC components.

        :param dict context: Additional widget attributes.
        """

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
        """Return an AST for a DateField/DateInput field/widget using
        MDC components.

        :param dict context: Additional widget attributes.
        """

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
        """Return an AST for a CharField/choices or ForeignKey/Select
        field/widget using MDC components.

        :param dict context: Additional widget attributes.
        """
        props, children = [], []
        props.append(
            cp("name", context['widget']['name']))

        for attr, value in context['widget']['attrs'].items():
            props.append(cp(attr, value))

        # Implementation of
        # django/forms/templates/django/forms/widgets/select.html.
        for group_name, group_choices, _ in \
                context["widget"]["optgroups"]:
            props_group, children_group = [], []
            if group_name:
                props_group = [cp("label", group_name)]

            for option in group_choices:
                props_option = []
                option_label = option["label"]
                # MDC: Override any instance of 'empty_label' as a
                # floating label will be displayed instead.
                if option["value"] == "":
                    option_label = ""
                props_option.append(
                    cp("value", str(option["value"])))
                for attr, value in option['attrs'].items():
                    props_option.append(cp(attr, value))
                children_group.append(
                    chp.Option(props_option, option_label))

            # Build a list of optgroups:
            if group_name:
                children.append(
                    chp.Optgroup(props_group, children_group))
            # Or a list of options:
            else:
                children.extend(children_group)

        return mdc.SelectField(props, children, context)
