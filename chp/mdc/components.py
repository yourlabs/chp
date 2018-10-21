
from .. import components as chp

from ..pyreact import (ce, cp, get_prop)

MDC_TYPE_MAP = {
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
    '''Wrap an element in an mdc-form-field.

    Only required for checkbox and radio button fields
    ''' 
    props = [
        cp("class", "mdc-form-field mdc-form-field--align-end"),
        cp("data-mdc-auto-init", "MDCFormField"),
    ]
    return Div(props, children)


def LineRipple():
    return Div([cp("class", "mdc-line-ripple")], [])


def Label(props=[], children=[], context={}):
    if children != []:
        if context.get("type", "text") not in ["checkbox"]:
            props.append(
                cp("class", "mdc-floating-label")
            )
        return chp.Label(props, children)
    else:
        return []


def Input(props=[], children=[]):
    props.append(
        cp("class", "mdc-text-field__input"),
    )
    return chp.Input(props, children)


def Checkbox(props=[], children=[], context={}):
    props.append(
        cp('class', 'mdc-checkbox__native-control')
    )
    ast_input = chp.Checkbox(props, children)

    props_field = [
        cp("class", "mdc-checkbox"),
        cp("data-mdc-auto-init", "MDCCheckbox"),
    ]
    children_field = [
        ast_input,
        Div([cp("class", "mdc-checkbox__background")], []),
    ]
    ast_field = Div(props_field, children_field)

    return ast_field


def CheckboxField(props=[], children=[], context={}):
    ast_checkbox = Checkbox(props, children, context)
    children_formfield = [ast_checkbox]

    label = context.get("label", "")
    if label != "":
        props_label = []
        el_id = get_prop(props, "id")
        if el_id is not None:
            props_label = [
                cp("for", el_id["value"]),
            ]
        ast_label = Label(props_label, label, context)
        children_formfield.append(ast_label)
    return FormField(children_formfield)


def InputField(props=[], children=[]):
    '''Receive props ("type") of the inner Input element
    and wrap the children in a new MDC Div.
    '''
    typ = get_prop(props, "type")
    if typ is None:
        typ = {"name": "type",
               "value": "text",
               }
    mdc_type = MDC_TYPE_MAP[typ["value"]]
    props_field = [
        cp("class", mdc_type["class"]),
        cp("data-mdc-auto-init", mdc_type["init"]),
    ]
    return Div(props_field, children)


def SubmitButton(props=[], children=[]):
    ast = chp.SubmitButton(props, children)
    props_div = [
        cp("class", "mdc-button"),
        cp("data-mdc-auto-init", None),
    ]
    return Div(props_div, ast)


def Select(props=[], children=[]):
    props.append(
        cp("class", "mdc-select__native-control")
    )
    return chp.Select(props, children)


def SelectField(props=[], children=[], context={}):
    ast = Select(props, children)
    children_field = [ast]
    label = context.get("label", "")
    if label != "":
        props_label = []
        el_id = get_prop(props, "id")
        if el_id is not None:
            props_label.append(
                cp("for", el_id["value"]))
        ast_label = Label(props_label, label, context)
        children_field.append(ast_label)
    children_field.append(LineRipple())
    props_field = [
        cp("type", "select")]
    return InputField(props_field, children_field)
