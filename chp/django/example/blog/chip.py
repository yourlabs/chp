from . import pyreact

ce = pyreact.create_element
cp = pyreact.create_prop

def Div(props, children):
    children = children or []
    return ce('div', props, children)


def Grid(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__inner')
    ]
    return Div(props, children)

def Row(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__inner')
    ]
    return Div(props, children)

def Cell(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__cell')
    ]
    return Div(props, children)

def Errors():
    props = []
    children='''
        {% for error in form.non_field_errors %}
            {{ error }}
        {% endfor %}
    '''
    return Div(props, children)

def Form(children):
    props = [
        cp('class', 'mdc-layout-grid__cell')
    ]
    errors=Errors()
    children.append(errors)
    return ce('form', props, children)


def Field(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-field')
    ]
    return Div(props, children)


def Input(value):
    props = [
        cp('class', 'mdc-input__native-control'),
        cp('type', 'text'),
        cp('id', '{{ id }}'),
        cp('value', value),
    ]
    return ce('input', props, [])

def Checkbox(is_checked):
    props = [
        cp('class', 'mdc-checkbox__native-control'),
        cp('type', 'checkbox'),
        cp('id', '{{ id }}'),
        cp('checked' if is_checked else '', ''),
    ]
    return ce('input', props, [])

def Label():
    def c(context):
        props = [
            cp('for', context),
        ]
        return ce('label', props, context)
    return c

def CheckboxField(isChecked):
    children = []
    props = [
        cp('class', 'mdc-form-field')
    ]
    children.append(Div(
            [cp("class", "mdc-checkbox")],
            [
                Checkbox(isChecked),
                Div(
                    [cp("class", "mdc-checkbox-background")],
                    []
                ),
                Label()
            ]
        ))
    return Div(props, children)

