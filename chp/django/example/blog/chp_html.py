from . import chp

ce = chp.create_element
cp = chp.create_prop

def Div(props, children):
    children = children or []
    return ce('div', props, children)

def Button(props, children):
    children = children or []
    return ce('div', props, children)

def Input(props):
    children = []
    return ce('input', props, children)

def Script(string = ""):
    return ce('script', [], string)

def ScriptBefore(children, script_text):
    children = children or []
    script = [Script(script_text)]
    children =  script.append(children)
    return Div([], children)


def Errors():
    props = []
    children='''
    '''
    return Div(props, children)

def Form(props, children):
    return ce('form', props, children)


def Label(name):
    def c(context):
        props = [
        ]
        return ce('label', props, context["label"] + " " + name)
    return c

