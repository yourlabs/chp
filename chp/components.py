from .pyreact import ce, cp, get_prop


def Div(props=[], children=[]):
    return ce('div', props, children)


def Para(props=[], children=[]):
    return ce('p', props, children)


def Button(props=[], children=[]):
    props.append(
        cp('type', 'button'))
    return ce('button', props, children)


def SubmitButton(props=[], children=[]):
    props.append(
        cp('type', 'submit'))
    if children == []:
        children = "Submit"
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


def Text(props=[], children=[]):
    props.append(
        cp('type', "text")
        )
    return Input(props, children)


def Label(props=[], children=[]):
    if children != []:
        return ce('label', props, children)
    else:
        return []


def Date(props=[], children=[]):
    props.append(
        cp('type', "date")
        )
    return Input(props, children)


def Select(props=[], children=[]):
    required = get_prop(props, "required")
    if required is not None:
        # find first option and disable it if it has no value
        try:
            props_option = children[0]["props"]
            option_value = get_prop(props_option, "value")
            if (option_value is None
                    or option_value["value"] == ""):
                props_option.append(
                    cp("disabled", True))
        except (Exception, ) as e:
            pass
    return ce('select', props, children)


def Option(props=[], children=[]):
    return ce("option", props, children)


def Optgroup(props=[], children=[]):
    return ce("optgroup", props, children)


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
