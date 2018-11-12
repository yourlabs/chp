
from .. import components as chp

from ..pyreact import (ce, cp, get_prop)

MDC_TYPE_MAP = {
    "checkbox": {
        "class": "mdc-checkbox",
        "init": "MDCCheckbox",
        },
    "text": {
        "class": "mdc-text-field",
        "init": "MDCTextField",
        },
    "date": {
        "class": "mdc-text-field",
        "init": "MDCTextField",
        },
    "select": {
        "class": "mdc-select",
        "init": "MDCSelect",
        },
}


def Div(props=[], children=[]):
    return chp.Div(props, children)


def Grid(children=[]):
    """Set the DMC display to 'grid'."""
    props = [
        cp('class', 'mdc-layout-grid')
    ]
    return Div(props, children)


def Row(children=[]):
    props = [
        cp('class', 'mdc-layout-grid__inner')
    ]
    return Div(props, children)


def Cell(children=[]):
    props = [
        cp('class', 'mdc-layout-grid__cell')
    ]
    return Div(props, children)


def Flex(props=[], children=[], context={}):
    """Set the MDC display to 'flex'."""
    display = context.get("display", "flex")
    props.append(
        cp("style", f"display: {display};")
    )
    return Div(props, children)


def Form(props=[], children=[]):
    ast = chp.Form(props, children)
    ast["props"].append(
        cp('class', 'mdc-layout-grid__cell')
    )
    return ast


def FormField(children=[]):
    """Wrap an element in an MDC FormField.

    Only required for checkbox and radio button fields
    """
    props = [
        cp("class", "mdc-form-field mdc-form-field--align-end"),
        cp("data-mdc-auto-init", "MDCFormField"),
    ]
    return Div(props, children)


def LineRipple():
    """Add an MDC Ripple effect."""
    return Div([cp("class", "mdc-line-ripple")], [])


def Label(props=[], children=[], context={}):
    """Add MDC class to a label element."""
    if children != []:
        if context.get("type", "text") not in ["checkbox"]:
            props.append(
                cp("class", "mdc-floating-label")
            )
        return chp.Label(props, children)
    else:
        return []


def Text(props=[], children=[]):
    """Add MDC class to a text input element."""
    props.append(
        cp("class", "mdc-text-field__input"),
    )
    return chp.Text(props, children)


def TextField(props=[], children=[], context={}):
    """Wrap a text input element with a label (from context) in an MDC Field.

    If a label is provided, find a "for" field id from context or else the
    input element id."""
    children_field = [
        Text(props, children)
    ]
    label = context.get("label", "")
    if label != "":
        props_label = []
        el_for = context.get("for", "")
        if el_for == "":
            el_for = get_prop(props, "id")
            if el_for is None:
                el_for = ""
            else:
                el_for = el_for["value"]
        if el_for != "":
            props_label = [cp("for", el_for)]
        ast_label = Label(props_label, label, context)
        children_field.append(ast_label)
    children_field.append(LineRipple())
    return InputField([], children_field, context)


def Date(props=[], children=[]):
    props.append(
        cp("class", "mdc-text-field__input"),
    )
    return chp.Date(props, children)


def DateField(props=[], children=[], context={}):
    """Wrap a date input element with a label (from context) in an MDC Field.

    If a label is provided, find a "for" field id from context or else the
    input element id."""
    children_field = [
        Date(props, children)
    ]

    label = context.get("label", "")
    if label != "":
        props_label = []
        el_for = context.get("for", "")
        if el_for == "":
            el_for = get_prop(props, "id")
            if el_for is None:
                el_for = ""
            else:
                el_for = el_for["value"]
        if el_for != "":
            props_label = [cp("for", el_for)]
        ast_label = Label(props_label, label, context)
        children_field.append(ast_label)
    children_field.append(LineRipple())
    return InputField([], children_field, context)


def Checkbox(props=[], children=[], context={}):
    """Wrap a checkbox input element with a default background
    in an MDC Field."""
    context.update({"type": "checkbox"})
    props.append(
        cp('class', 'mdc-checkbox__native-control')
    )
    ast_input = chp.Checkbox(props, children)

    children_field = [
        ast_input,
        Div([cp("class", "mdc-checkbox__background")], []),
    ]
    return InputField([], children_field, context)


def CheckboxField(props=[], children=[], context={}):
    """Wrap a checkbox MDC field with a label (from context)
    in an MDC FormField.

    If a label is provided, find a "for" field id from context or else the
    input element id."""
    ast_checkbox = Checkbox(props, children, context)
    children_formfield = [ast_checkbox]

    label = context.get("label", "")
    if label != "":
        props_label = []
        el_for = context.get("for", "")
        if el_for == "":
            el_for = get_prop(props, "id")
            if el_for is None:
                el_for = ""
            else:
                el_for = el_for["value"]
        if el_for != "":
            props_label = [cp("for", el_for)]
        ast_label = Label(props_label, label, context)
        children_formfield.append(ast_label)
    return FormField(children_formfield)


def InputField(props=[], children=[], context={}):
    """Wrap the children in an MDC input field.

    Requires context["type"] to lookup MDC classes."""
    el_type = context.get("type", "text")
    mdc_type = MDC_TYPE_MAP[el_type]
    props_field = [
        cp("class", mdc_type["class"]),
        cp("data-mdc-auto-init", mdc_type["init"]),
    ]
    return Div(props_field, children)


def SubmitButton(props=[], children=[]):
    """Wrap a submit button in an MDC field."""
    ast = chp.SubmitButton(props, children)
    props_div = [
        cp("class", "mdc-button"),
        cp("data-mdc-auto-init", None),
    ]
    return Div(props_div, ast)


def Select(props=[], children=[]):
    """Add MDC class to a Select element."""
    props.append(
        cp("class", "mdc-select__native-control")
    )
    return chp.Select(props, children)


def SelectField(props=[], children=[], context={}):
    """Wrap a Select element with a label (from context) in an MDC Field.

    If a label is provided, find a "for" field id from context or else the
    select element id."""
    context.update({"type": "select"})
    ast = Select(props, children)
    children_field = [ast]
    # add a label add label (optional) and find a "for" field id
    label = context.get("label", "")
    if label != "":
        props_label = []
        el_for = context.get("for", "")
        if el_for == "":
            el_for = get_prop(props, "id")
            if el_for is None:
                el_for = ""
            else:
                el_for = el_for["value"]
        if el_for != "":
            props_label = [cp("for", el_for)]
        ast_label = Label(props_label, label, context)
        children_field.append(ast_label)
    children_field.append(LineRipple())
    return InputField([], children_field, context)
