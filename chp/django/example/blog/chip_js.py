import chp

ce = chp.create_element
cp = chp.create_prop
def cjs(props, children):
    return ce('js', props, children)

def instruction(value):
    props = [
        cp('before', f'('),
        cp('after', ');'),
    ]
    children = value if type(value) is str else [value]
    return cjs(props, children)

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
    # def_local('a', '1'),
    # def_global('a', '1'),
    # instruction(op('+', '1', '2')),
    # If('a === 2', i),
    def_local('x', 'document.getElementById(\'mySelect\').value'),
    assign('document.getElementById(\'demo\').innerHTML', op('+', "'You selected: '", 'x')),
    Return('a')
]
ast = def_local('a', '1')
# ast = def_global('foo', def_func("foo", "a, b", [def_func("bar", "c, d, e", content)]))
ast = def_func("f", "", content)
js = chp.render_js_element(ast)
print(js)

# (function() {var x = })
