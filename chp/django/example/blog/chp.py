##########
## PYREACT
##########


def get_prop(props=[], name=[]):
    for p in props:
        try:
            if p["name"] == name:
                return p
        except KeyError:
            return None

# returns a middleware. a middleware is a function that takes and ast element and returns an other ast element
# in the case of this middleware, we inspect the type of el and call it with a context.
# with this middlware a component can now return a function taking a context as argument and returning an el.
def context_middleware(context):

    def middleware(el):
        if callable(el):
            return el(context)
        else:
            return el
    return middleware

def default_middleware(el, _props = [], _children=[]):
    return el


def render_html(el, props, child):
    name = el["name"]

    children = ""
    for c in child:
        children += c

    props_str = ""
    for p in props:
        if p["name"] != "children":
            props_str += (p["name"] + "=\"" + p["value"] + "\"")

    self_closing_tags = ["input", "link", "img"]
    if name in self_closing_tags:
        return f"<{name} {props_str} />"

    return f"<{name} {props_str}>{children}</{name}>"

def render_ast(ast, ast_middleware, render_middleware):
    ast = ast_middleware(ast)

    props = ast["props"]

    children = False
    for p in props:
        if p["name"] == "children":
            children = p["value"]

    child = []
    if not children:
        child = ""
    elif type(children) is str:
        child = children
    else:
        for c in children:
            child.append(render_ast(c, ast_middleware, render_middleware))

    return render_middleware(ast, props, child)

def render_element(ast, middleware=default_middleware):
    return render_ast(ast, middleware, render_html)

def create_element(name, props, children):
    props.append({
        "name": "children",
        "value": children,
    })

    return {
        "name": name,
        "props": props,
    }

def create_prop(name, value):
    return {
        "name": name,
        "value": value,
    }

def create_context(value):
    return [{
            "name": "__context",
            "value": value,
        }]