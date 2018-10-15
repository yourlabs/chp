
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


def Form(props, children):
    ast = chp.Form(props, children)
    ast["props"].append(
        cp('class', 'mdc-layout-grid__cell')
    )
    return ast


def FormField(children):
    props = [
        cp("class", "mdc-form-field mdc-form-field--align-end"),
        cp("data-mdc-auto-init", "MDCFormField"),
    ]
    return Div(props, children)


def LineRipple():
    return Div([cp("class", "mdc-line-ripple")], [])


def Label(props, children=[], context={}):
    if children != []:
        if context.get("type", "text") not in ["checkbox"]:
            props.append(
                cp("class", "mdc-floating-label")
            )
        return chp.Label(props, children)
    else:
        return []


def Input(props, children):
    props.append(
        cp("class", "mdc-text-field__input"),
    )
    return chp.Input(props, children)


def Checkbox(props, children, context={}):
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


def CheckboxField(props, children, context={}):
    ast_checkbox = Checkbox(props, children, context)
    children_formfield = [ast_checkbox]
    label = context.get("label", "")
    if label != "":
        el_id = get_prop(props, "id")
        if el_id is not None:
            lbl_props = [
                cp("for", el_id["value"]),
            ]
        ast_label = Label(lbl_props, label, context)
        children_formfield.append(ast_label)
    return FormField(children_formfield)


def InputField(props, children=[]):
    typ = get_prop(props, "type")
    mdc_type = MDC_TYPE_MAP[typ["value"]]
    props = [
        cp("class", mdc_type["class"]),
        cp("data-mdc-auto-init", mdc_type["init"]),
    ]
    return Div(props, children)


def SubmitButton(props, children):
    ast = chp.SubmitButton(props, children)
    props = [
        cp("class", "mdc-button"),
        cp("data-mdc-auto-init", None),
    ]
    return Div(props, ast)
