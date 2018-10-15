from .pyreact import *
from pyreact import get_prop


def Div(props, children):
    children = children or []
    return ce('div', props, children)


def Button(props=[], children=[]):
    props.append(
        cp('type', 'button'))
    return ce('button', props, children)


def SubmitButton(props=[], children=[]):
    props.append(
        cp('type', 'submit'))
    return ce('button', props, children)


def Script(string=""):
    return ce('script', [], string)


def ScriptBefore(children, script_text):
    children = children or []
    script = [Script(script_text)]
    children = script.append(children)
    return Div([], children)


def Form(props=[], children=[]):
    return ce('form', props, children)


def Errors():
    props = []
    children = '''
    '''
    return Div(props, children)


def Input(props=[], children=[]):
    return ce('input', props, children)


def Checkbox(props=[], children=[]):
    props.append(
        cp('type', "checkbox")
        )
    return Input(props, children)


def Label(props=[], children=[]):
    if children != []:
        return ce('label', props, children)
    else:
        return []


# def Label(name):
#     def c(context):
#         props = [
#         ]
#         return ce('label', props, context["label"] + " " + name)
#     return c


# def CheckboxField(isChecked):
#     def c(context):
#         children = []
#         props = [
#             cp('class', 'mdc-form-field')
#         ]
#         children.append(Div(
#             [cp("class", "mdc-checkbox")],
#             [
#                 Checkbox(isChecked),
#                 Div(
#                     [cp("class", "mdc-checkbox-background")],
#                     []
#                 ),
#                 Label('Checkbox'),
#                 Label(context["label"])
#             ]
#         ))
#         return Div(props, children)
#     return c
