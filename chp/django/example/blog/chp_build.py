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

def default_middleware(el):
    return el

def render_html(el, props, child):
    name = el["name"]
    props_str = ""
    for p in props:
        if p["name"] != "children":
            props_str += (p["name"] + "=\"" + p["value"] + "\"")

    self_closing_tags = ["input", "link", "img"]
    if name in self_closing_tags:
        return f"<{name} {props_str} />"
    print('heey')

    return f"<{name} {props_str}>{child}</{name}>"

def render_js(el, props, child):
    name = el["name"]
    props_str = ""

    before=get_prop(props, "before")["value"]
    after=get_prop(props, "after")["value"]

    return f"{before}{child}{after}"

def render_ast(ast, ast_middleware, render_middleware):
    ast = ast_middleware(ast)

    props = ast["props"]

    children = False
    for p in props:
        if p["name"] == "children":
            children = p["value"]

    child = ""
    if not children:
        child = ""
    elif type(children) is str:
        child = children
    else:
        for c in children:
            child += render_ast(c, ast_middleware, render_middleware)

    return render_middleware(ast, props, child)

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





def create_store(store_name, on_store_change):
    onchange_cb = store_name + "_cb"
    code = [
        def_global(onchange_cb, def_func("f", "obj, prop", on_store_change)),
        def_global(
            store_name,
            '!window.todoStore ? new Proxy({}, { set: (obj, prop, value) => {obj[prop]=value;window.'+onchange_cb+'(obj, prop); return true } }) : window.todoStore'
        ),
    ]
    ast = progn(code)
    js = render_js_element(ast)
    return js

def render_app(store_name):
    return progn([
        def_local("str", f"render_ast(FormSchema(window.{store_name}), default_middleware, render_html)"),
        assign("document.querySelector('body').innerHTML", "str"),
        progn("eval(document.querySelector('body script').innerHTML);"),
    ])




####### todos.py





def SubmitButton(name, on_click):
    props = [
        cp('onclick', on_click)
    ]
    return Div(props, name)

def TodoItem(name, todo_id):
    def remove_todo():
        ast = progn([
            instruction(f"todos = window.todoStore.todos || []"),
            instruction(f"todos = todos.filter(t => t.id !== {todo_id})"),
            instruction(f"window.todoStore.todos = [...todos]"),
        ])
        return render_js_element(ast)

    props = [
        cp("id", todo_id),
        cp("style", "margin: 1rem; height: 3rem; background-color: rgba(0, 0, 0, 0.2); border: 2px solid black"),
        cp("onclick", remove_todo()),
    ]
    return Div(props, name)

def Input(value):
    def update_label_value():
        content = [
            def_local('x', 'document.getElementById(`myInput`).value'),
            instruction("window.todoStore.name=x"),
        ]
        ast = call_anonymous(def_func("f", "", content))
        js = render_js_element(ast)
        return js

    props = [
        cp('type', 'text'),
        cp('onkeyup', update_label_value()),
        cp('id', 'myInput'),
        cp('value', value),
        cp('onfocus', "(()=>{let value = this.value;this.value=''; this.value = value})()")
    ]
    return ce('input', props, [])


def FormSchema(store_content):
    store_name = "todoStore"
    store_change_cb = [
        render_app(store_name),
        progn("document.querySelector('#myInput').focus()"), # FIX => quick input focus had on rerender
    ]

    def update_todos():
        ast = progn([
            def_local("t", "window.todoStore.todos ? window.todoStore.todos : []"),
            assign(
                "window.todoStore.todos",
                "[...t, {name: window.todoStore.name, id: t.length - 1}]",
            ),
            assign("window.todoStore.name", "''"),
        ])
        js = render_js_element(ast)
        return js

    def render():
        form = Form([
            Cell([
                Div(
                    [cp("style", "display: flex;")],
                    [
                        Input(store_content["name"]),
                        SubmitButton("Submit", update_todos()),
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
                Script(create_store(store_name, store_change_cb)),
                form,
                Div([], reversed(todos)),
            ],
        )

    return render()
