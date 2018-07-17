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
def cjs(props, children):
    return ce('js', props, children)

def progn(content):
    return call_anonymous(def_func("f", "", content))

def call_anonymous(value):
    props = [
        cp('before', '('),
        cp('after', ')()'),
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
    errors go here
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


def Input(value, subscribe_store_change):
    def update_label_value():
        content = [
            def_local('x', 'document.getElementById(`myInput`).value'),
            log('`hey` + x'),
            instruction("window.todoStore.name=x"),
        ]
        ast = call_anonymous(def_func("f", "", content))
        js = render_js_element(ast)
        return js

    subscribe_store_change([
        log('`killer`'),
        log('`keydown`'),
        instruction('window.todoStore.name === `foo` ? document.getElementById(`demo`).innerHTML = "you won" : document.getElementById(`demo`).innerHTML = ""'),
    ])

    props = [
        cp('type', 'text'),
        cp('onkeyup', update_label_value()),
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


####### TODO.py





def create_store(store_name, on_store_change):
    onchange_cb = store_name + "_cb"
    code = [
        def_global(onchange_cb, def_func("f", "obj, prop", on_store_change)),
        def_global(
            store_name,
            'new Proxy({}, { set: (obj, prop, value) => {obj[prop]=value;window.'+onchange_cb+'(obj, prop); return true } })'
        ),
    ]
    ast = progn(code)
    js = render_js_element(ast)
    return js

def FormSchema(store_content):
    store_name = "todoStore"
    store_change_func_content = [
        log('obj[prop]'),
        progn(
            "for(let key in chp_build) { window[key] = chp_build[key]};" +
            "str = render_ast(FormSchema(window.todoStore), default_middleware, render_html);" +
            "document.querySelector('body').innerHTML = str;" +
            "eval(document.querySelector('body script').innerHTML);"
        )
    ]
    def update_label_value():
        content = [
            def_local('x', 'document.getElementById(\'myInput\').value'),
            log('x'),
            assign('document.getElementById(\'demo\').innerHTML', op('+', "'You selected: '", 'x')),
        ]
        ast = progn(content)
        js = render_js_element(ast)
        return js

    def get_on_store_change():
        return store_change_func_content

    def get_js():
        return create_store(store_name, get_on_store_change())

    def subscribe_store_change(content):
        for c in content:
            store_change_func_content.append(c)

    def render():
        form = Form([
            Cell([
                Input(store_content["name"], subscribe_store_change),
                Div(
                    [create_prop("style", "height: 5rem")],
                    "If you type <strong>foo</strong> in the textbox and unfocus, your secret message will appear !!"
                ),
                Div([create_prop("id", "demo"), create_prop("style", "color: red")], ""),
            ])
        ])

        return Div(
            [],
            [
                Script(get_js()),
                form,
            ],
        )

    return render()
