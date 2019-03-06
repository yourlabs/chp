
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


def Grid(props=[], children=[]):
    """Start the MDC grid layout."""
    props.append(
        cp('class', 'mdc-layout-grid')
    )
    return Div(props, children)


def Row(props=[], children=[]):
    """Start the MDC grid inner."""
    props.append(
        cp('class', 'mdc-layout-grid__inner')
    )
    return Div(props, children)


def Cell(props=[], children=[], context={}):
    """Start the MDC grid cell.

    Set the span to 12 columns as a sensible default."""
    span = context.get("span", 12)
    props.append(
        cp('class', f'mdc-layout-grid__cell--span-{span}')
    )
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
    # ast["props"].append(
    #     cp('class', 'mdc-layout-grid__cell')
    # )
    return ast


def FormField(children=[]):
    """Wrap an element in an MDC FormField.

    Only required for checkbox and radio button fields
    """
    props = [
        cp("class", "mdc-form-field mdc-form-field--align-left"),
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
    mdc_class = mdc_type["class"]

    # if there are errors, add --invalid class.
    if context["errors"]:
        mdc_invalid = "mdc-text-field--invalid"
        mdc_class = f"{mdc_class} {mdc_invalid}"

    props_field = [
        cp("class", mdc_class),
        cp("data-mdc-auto-init", mdc_type["init"]),
    ]

    return Div(props_field, children)


def SubmitButton(props=[], children=[]):
    """Wrap a submit button in an MDC field."""
    props.append(
        cp("class", "mdc-button"))
    ast = chp.SubmitButton(props, children)
    return ast


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


def HelperText(props=[], children=[], context={}):
    """Add MDC classes to help text for an input field.

    Use 'name' from 'context' to link the text to an input  field.
    <div class="mdc-text-field-helper-line">
      <div id="{field_name}-helper-text"
        class="mdc-text-field-helper-text
          mdc-text-field-helper-text--persistent
          mdc-text-field-helper-text--validation-msg"
        aria-hidden="true">
        {message}
      </div>
    </div>
    """
    field_name = context.get("name", "")

    classes = chp.get_prop(props, "class")
    if classes is None:
        classes = []
    else:
        classes = classes["value"]
        if isinstance(classes, (str,)):
            classes = [classes]

    classes.extend([
        "mdc-text-field-helper-text",
        "mdc-text-field-helper-text--persistent",
    ])
    # prepend new 'class' prop to supercede original entry in list.
    # TODO: add set_prop() functionality?
    props = [cp("class", " ".join(classes))] + props
    sep = "-"
    props.append(
        cp("id",
           f"{(field_name + sep) if field_name else 'non-field-'}helper-text")
    )
    children_line = [chp.Div(props, children)]

    props_line = [cp("class", "mdc-text-field-helper-line"),]
    return chp.Div(props_line, children_line)

def ValidationText(props=[], children=[], context={}):
    """Add MDC classes to validation text for an input field.
    
    Use 'name' from 'context' to link to an input field and display 'errors'."""
    props = [
        cp("class", "mdc-text-field-helper-text--validation-msg"),
    ]

    children = "<br />".join(context.get("errors", []))
    return HelperText(props, children, context)
