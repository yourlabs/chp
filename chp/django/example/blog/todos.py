import chp

chip_js = chp.chip_js
pyreact = chp.pyreact

ce = pyreact.create_element
cp = pyreact.create_prop

def_global = chip_js.def_global
def_local = chip_js.def_local
def_func = chip_js.def_func
assign = chip_js.assign
op = chip_js.op
op = chip_js.op
progn = chip_js.progn
call_anonymous = chip_js.call_anonymous




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
    js = pyreact.render_js_element(ast)
    return js

def FormSchema(value):
    store = "todoStore"
    store_change_func_content = [
        chip_js.log('obj[prop]'),
    ]
    def update_label_value():
        content = [
            def_local('x', 'document.getElementById(\'myInput\').value'),
            chip_js.log('x'),
            assign('document.getElementById(\'demo\').innerHTML', op('+', "'You selected: '", 'x')),
        ]
        ast = progn(content)
        js = pyreact.render_js_element(ast)
        return js

    def get_on_store_change():
        return store_change_func_content

    def get_js():
        return create_store(store, get_on_store_change())

    def subscribe_store_change(content):
        nonlocal store_change_func_content
        store_change_func_content += content

    def render():
        return chp.ScriptBefore(
            [
                chp.Form([
                    chp.Cell([
                        chp.Input('username', subscribe_store_change),
                        chp.Div(
                            [chp.create_prop("style", "height: 5rem")],
                            "If you type <strong>foo</strong> in the textbox and unfocus, your secret message will appear !!"
                        ),
                        chp.Div([chp.create_prop("id", "demo"), chp.create_prop("style", "color: red")], ""),
                    ])
                ])
            ],
            get_js(),
        )

    return render()
