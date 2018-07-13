from pyreact import create_element, create_prop, render_element

ce = create_element
cp = create_prop

def Text(t):
    return ce("span", [], t)

def Error(str=""):
    style=cp("style", "color: red")
    return ce("span", [style], str)

def Input(label, value, input_type, errors=[]):
    is_error=False
    if len(errors):
        is_error=True

    # Creating children
    inputComp=Text(value)
    label=Text(label)
    children = [label, inputComp]
    for e in errors:
        children.append(Error(e))

    style="color:green" if is_error else ""
    props=[
        cp("style", style),
        cp("type", input_type),
    ]

    return ce('div', props, children)

def Form(form):
    fields=form["fields"]
    children = [] # menu children links array
    for i in fields:
        el = Input(i["label"], i["value"], i["type"], i["errors"])
        children.append(el)

    errors=form["errors"]
    if len(errors):
        for e in errors:
            children.append(Error(e))

    props=[
        cp("class", "form"),
    ]
    return ce("form", props, children)


def Body(form):
    children = [Form(form)] # body children
    props = []

    return ce("body", props, children)

def App(form):
    children = [Body(form)]
    props = []

    return ce("html", props, children)
