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

import math
import random


def diff_asts(old, new):
    patches = []
    new_tree = {}
    old_name = old["name"]
    old_props = old["props"]
    new_name = new["name"]
    new_props = new["props"]

    # if elements not same name
        # request to patch innerHTML with chp-id of the old one

    if old_name != new_name:
        patches.append({
            "type": "replace-element",
            "chp-id": get_prop(old_props, "chp-id")["value"],
            "html": render_element(new),
        })
        new_tree = new
        # id = get_prop('chp-id', new_tree["props"])
        # id["value"] = get_prop('chp-id', new["props"])["value"]

    # else
        # go through props
        # excluding children
        # if props differ
            # request patching with new props (but keep old chp-id)

    else:
        i = 0
        props_differ = False
        if len(old_props) != len(new_props):
            props_differ = True

        if not props_differ:
            while i < len(new_props):
                c1 = old_props[i]["name"] == new_props[i]["name"]
                c2 = old_props[i]["value"] == new_props[i]["value"]
                if not (c1 and c2):
                    if new_props[i]["name"] != "children":
                        if new_props[i]["name"] != "chp-id":
                            props_differ = True
                i += 1

        if props_differ:
            id = get_prop(new_props, "chp-id")
            id["value"] = get_prop(old_props, "chp-id")["value"]
            patches.append({
                "type": "props",
                "chp-id": get_prop(old_props, "chp-id")["value"],
                "props" : new_props
            })
            new_tree = new
            new_tree["props"] = new_props
        else:
            new_tree = old


    nc = get_prop(new_props, "children")
    oc = get_prop(old_props, "children")
    new_children =  nc["value"] if nc else []
    old_children =  oc["value"] if oc else []

    if len(new_children) != len(old_children):
        html = ""
        if type(new_children) is str:
            html = new_children
        else:
            for c in new_children:
                html += render_element(c)
                # new_tree
                new_tree_children = get_prop(new_tree["props"], 'children') # ref to new_tree's props
                new_tree_children["value"] = get_prop(new["props"], 'children')["value"] # now ref to new's props


        patches.append({
            "type": "innerHTML",
            "chp-id": get_prop(old_props, "chp-id")["value"],
            "html": html,
        })
    else:
        new_tree_children = get_prop(new_tree["props"], 'children') # ref to new_tree's props
        new_tree_children = get_prop(new["props"], 'children') # ref to new_tree's props
        if type(new_children) is str:
            new_tree_children["value"] = new_children
        else:
            i = 0
            while i < len(new_children):
                child_diff = diff_asts(old_children[i], new_children[i])
                ps = child_diff[0]
                for p in ps:
                    patches.append(p)
                i += 1

                new_tree_children["value"] = child_diff[1]

    # go through children
        # if new one missing
            # request deletion of old node (with chp-id)

        # if old one missing
            # request creation of new node

    return [patches, new_tree]


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
    print('heey')

    return f"<{name} {props_str}>{children}</{name}>"

def render_js(el, props, child):
    name = el["name"]
    props_str = ""

    children = ""
    for c in child:
        children += c

    before=get_prop(props, "before")["value"]
    after=get_prop(props, "after")["value"]

    return f"{before}{children}{after}"

def id_middleware(ast):
    props = ast["props"]
    props.append({
        "name": "chp-id",
        "value": str(math.floor(random.random()*10000000))
    })
    return ast


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

def inject_ids(ast):
    return render_ast(ast, id_middleware, default_middleware)

def render_js_element(ast):
    return render_ast(ast, default_middleware, render_js)

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

def get_prop(props=[], name=[]):
    for p in props:
        try:
            if p["name"] == name:
                return p
        except KeyError:
            return None

def create_context(value):
    return [{
            "name": "__context",
            "value": value,
        }]









##########
## CHIP JS
##########





ce = create_element
cp = create_prop
def cjs(props, children): # create js element
    return ce('js', props, children)

def progn(content):
    return call_anonymous(def_func("f", "", content))

def call_anonymous(value):
    props = [
        cp('before', '('),
        cp('after', ')();'),
    ]
    children = value if type(value) is str else [value]
    return cjs(props, children)

def instruction(value):
    props = [
        cp('before', f'('),
        cp('after', ');'),
    ]
    children = value if type(value) is str else [value]
    return cjs(props, children)

def log(value):
    props = [
        cp('before', 'console.log('),
        cp('after', ')'),
    ]
    children = value
    return instruction(cjs(props, children))


def block(value):
    props = [
        cp('before', '{'),
        cp('after', '}'),
    ]
    children = value if type(value) is str else [value]
    return cjs(props, children)

def def_global(name, value):
    props = [
        cp('before', f'window.{name}='),
        cp('after', ''),
    ]
    children = [instruction(value)]
    return cjs(props, children)

def def_local(name, value):
    props = [
        cp('before', f'let {name}='),
        cp('after', ''),
    ]
    children = [instruction(value)]
    return cjs(props, children)

def assign(name, value):
    props = [
        cp('before', f'{name}='),
        cp('after', ''),
    ]
    children = [instruction(value)]
    return cjs(props, children)

def def_func(name, arguments, children):
    props = [
        cp('before', 'function(' + arguments + ') {'),
        cp('after', '}'),
    ]
    return cjs(props, children)

def If(condition, children):
    props = [
        cp('before', 'if(' + condition + ') {'),
        cp('after', '}'),
    ]
    return cjs(props, children)

def Return(children):
    props = [
        cp('before', 'return '),
        cp('after', ''),
    ]
    return cjs(props, [instruction(children)])

def op(operation, operand, operee):
    props = [
        cp('before', f'({operand} {operation} '),
        cp('after', f'{operee})'),
    ]
    children=""
    return cjs(props, children)


i = instruction(op('+', '1', '2')),
content = [
    def_local('x', 'document.getElementById(\'mySelect\').value'),
    assign('document.getElementById(\'demo\').innerHTML', op('+', "'You selected: '", 'x')),
]
ast = def_local('a', '1')
ast = call_anonymous(def_func("f", "", content))
js = render_js_element(ast)





##########
## CHIP HTML



def Div(props, children):
    children = children or []
    return ce('div', props, children)

def Button(props, children):
    children = children or []
    return ce('div', props, children)

def Script(string = ""):
    return ce('script', [], string)

def ScriptBefore(children, script_text):
    children = children or []
    script = [Script(script_text)]
    children =  script.append(children)
    return Div([], children)


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


####### store.py





def create_store(store_name, on_store_change, json_init_state):
    onchange_cb = store_name + "_cb"
    code = [
        def_global(onchange_cb, def_func("f", "obj, prop", on_store_change)),
        def_global(
            store_name,
            "!window.todoStore ? new Proxy(JSON.parse('" + json_init_state + "'), { set: (obj, prop, value) => {obj[prop]=value;window."+onchange_cb+"(obj, prop); return true } }) : window.todoStore"
        ),
    ]
    ast = progn(code)
    js = render_js_element(ast)
    return js

def patch_dom(patches):
    for patch in patches:
        type = patch["type"]
        chp_id = patch["chp-id"]
        if type == "props":
            props = patch["props"]
            for prop in props:
                el = document["querySelector"](f"[chp-id='{chp_id}']")
                if props["name"] != "chp-id":
                    el.setAttribute(prop["name"], prop["value"])
        elif type == "innerHTML":
            el = document["querySelector"](f"[chp-id='{chp_id}']")
            el.innerHTML = patch["html"]


def render_app(store_name, store_content_json):
    return progn([
        def_local("old_asttt", "window.asttt ? window.asttt : JSON.parse(document.querySelector(\"[chp-id='chp-ast']\").innerHTML)"),
        def_local("new_asttt", f"inject_ids(FormSchema(window.{store_name}, '{store_content_json}'))"),
        def_local("[patches, new_ast_from_diff]", "old_asttt ? window.diff_asts(old_asttt, new_asttt) : false"),
        def_global("asttt", "new_ast_from_diff"),
        log('patches, new_ast_from_diff'),
        progn("patches ? patch_dom(patches) : false"),
        def_local("html", f"render_element(window.asttt)"),
        # assign("document.querySelector('body').innerHTML", "html"),
        progn("eval(document.querySelector('body script').innerHTML);"),
    ])




####### todos.py



## Store manipulations

def remove_todo(todo_id):
    todos = todoStore["todos"] or []
    todos = list(filter(lambda t: parseInt(t["id"]) != todo_id, todos))
    todoStore.todos = todos

def update_todo_name():
    x = document["getElementById"]('myInput')
    todoStore["name"] = x["value"]

def add_todo(todoStore):
    todos = todoStore.todos or []
    t = todos[:]
    t.append({ "name" : todoStore["name"], "id": t.length})
    todoStore["todos"] = t
    todoStore["name"] = ""


store_updates = {
    "add_todo": add_todo,
    "remove_todo": remove_todo,
    "update_todo_name": update_todo_name,
}

## Components

def SubmitButton(name, on_click):
    props = [
        cp('onclick', on_click)
    ]
    return Button(props, name)


def TodoItem(name, todo_id):
    on_click = f"store_updates.remove_todo({todo_id})"
    props = [
        cp("id", todo_id),
        cp("style", "margin: 1rem; height: 3rem; background-color: rgba(0, 0, 0, 0.2); border: 2px solid black"),
        cp("onclick", on_click),
    ]
    return Div(props, name)


def Input(value):
    on_key_up = "store_updates.update_todo_name()"
    focus_hack = "(()=>{let value = this.value;this.value=\'\'; this.value = value})()"

    props = [
        cp('type', 'text'),
        cp('onkeyup', on_key_up),
        cp('id', 'myInput'),
        cp('value', value),
        # cp('onfocus', focus_hack)
    ]
    return ce('input', props, [])

def FormSchema(store_content, store_content_json):
    store_name = "todoStore"
    store_change_cb = [
        render_app(store_name, store_content_json),
        # progn("document.querySelector('#myInput').focus()"), # FIX => quick input focus had on rerender
    ]

    def add_todos():
        return f"store_updates.add_todo({store_name})"

    def render():
        form = Form([
            Cell([
                Div(
                    [cp("style", "display: flex;")],
                    [
                        Input(store_content["name"]),
                        SubmitButton("Submit", add_todos()),
                    ],
                ),
                Div(
                    [create_prop("style", "height: 5rem")],
                    "If you type <strong>foo</strong> in the textbox and unfocus, your secret message will appear !!"
                ),
                Div([create_prop("id", "demo"), create_prop("style", "color: red" if store_content["name"] == "foo" else "color: green")], "what color am I ?"),
            ])
        ])

        todos = []
        for t in store_content["todos"]:
            todos.append(TodoItem(t["name"], t["id"]))

        return Div(
            [],
            [
                Script(create_store(store_name, store_change_cb, store_content_json)),
                form,
                Div([], todos),
            ],
        )

    return render()

def AST(json_ast):
    children = json_ast
    props = [
        cp('style', 'display: none'),
        cp('chp-id', 'chp-ast'),
    ]
    return Div(props, children)


def injectAstIntoDOM(ast):
    window.asttt = ast


def Inject_ast_into_DOM(app, json_ast):
    children = [
        app,
        AST(json_ast),
        Script("window.asttt = JSON.parse(document.querySelector(\"[chp-id='chp-ast']\").innerHTML)"),
    ]
    return Div([], children)
