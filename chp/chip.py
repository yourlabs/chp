from . import pyreact
from . import chip_js

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


def_local = chip_js.def_local
def_func = chip_js.def_func
assign = chip_js.assign
op = chip_js.op
call_anonymous = chip_js.call_anonymous
def Input(value):
    def create_js():
        content = [
            def_local('x', 'document.getElementById(\'myInput\').value'),
            chip_js.log('x'),
            assign('document.getElementById(\'demo\').innerHTML', op('+', "'You selected: '", 'x')),
        ]
        ast = call_anonymous(def_func("f", "", content))
        js = pyreact.render_js_element(ast)
        return js

    props = [
        cp('type', 'text'),
        cp('onchange', create_js()),
        cp('id', 'myInput'),
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

def Label(name):
    def c(context):
        props = [
        ]
        return ce('label', props, context["label"] + " " + name)
    return c

def CheckboxField(isChecked):
    def c(context):
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
                    Label('Checkbox'),
                    Label(context["label"])
                ]
            ))
        return Div(props, children)
    return c

