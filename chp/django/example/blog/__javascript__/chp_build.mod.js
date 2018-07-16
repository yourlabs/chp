	(function () {
		var __name__ = '__main__';
		var get_prop = function (props, py_name) {
			if (typeof props == 'undefined' || (props != null && props .hasOwnProperty ("__kwargtrans__"))) {;
				var props = list ([]);
			};
			if (typeof py_name == 'undefined' || (py_name != null && py_name .hasOwnProperty ("__kwargtrans__"))) {;
				var py_name = list ([]);
			};
			var __iterable0__ = props;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var p = __iterable0__ [__index0__];
				try {
					if (p ['name'] == py_name) {
						return p;
					}
				}
				catch (__except0__) {
					if (isinstance (__except0__, KeyError)) {
						return null;
					}
					else {
						throw __except0__;
					}
				}
			}
		};
		var context_middleware = function (context) {
			var middleware = function (el) {
				if (callable (el)) {
					return el (context);
				}
				else {
					return el;
				}
			};
			return middleware;
		};
		var default_middleware = function (el) {
			return el;
		};
		var render_html = function (el, props, child) {
			var py_name = el ['name'];
			var props_str = '';
			var __iterable0__ = props;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var p = __iterable0__ [__index0__];
				if (p ['name'] != 'children') {
					props_str += ((p ['name'] + '="') + p ['value']) + '"';
				}
			}
			var self_closing_tags = list (['input', 'link', 'img']);
			if (__in__ (py_name, self_closing_tags)) {
				return '<{} {} />'.format (py_name, props_str);
			}
			print ('heey');
			return '<{} {}>{}</{}>'.format (py_name, props_str, child, py_name);
		};
		var render_js = function (el, props, child) {
			var py_name = el ['name'];
			var props_str = '';
			var before = get_prop (props, 'before') ['value'];
			var after = get_prop (props, 'after') ['value'];
			return '{}{}{}'.format (before, child, after);
		};
		var render_ast = function (ast, ast_middleware, render_middleware) {
			var ast = ast_middleware (ast);
			var props = ast ['props'];
			var children = false;
			var __iterable0__ = props;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var p = __iterable0__ [__index0__];
				if (p ['name'] == 'children') {
					var children = p ['value'];
				}
			}
			var child = '';
			if (!(children)) {
				var child = '';
			}
			else if (py_typeof (children) === str) {
				var child = children;
			}
			else {
				var __iterable0__ = children;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var c = __iterable0__ [__index0__];
					child += render_ast (c, ast_middleware, render_middleware);
				}
			}
			return render_middleware (ast, props, child);
		};
		var render_js_element = function (ast) {
			return render_ast (ast, default_middleware, render_js);
		};
		var render_element = function (ast, middleware) {
			if (typeof middleware == 'undefined' || (middleware != null && middleware .hasOwnProperty ("__kwargtrans__"))) {;
				var middleware = default_middleware;
			};
			return render_ast (ast, middleware, render_html);
		};
		var create_element = function (py_name, props, children) {
			props.append (dict ({'name': 'children', 'value': children}));
			return dict ({'name': py_name, 'props': props});
		};
		var create_prop = function (py_name, value) {
			return dict ({'name': py_name, 'value': value});
		};
		var get_prop = function (props, py_name) {
			if (typeof props == 'undefined' || (props != null && props .hasOwnProperty ("__kwargtrans__"))) {;
				var props = list ([]);
			};
			if (typeof py_name == 'undefined' || (py_name != null && py_name .hasOwnProperty ("__kwargtrans__"))) {;
				var py_name = list ([]);
			};
			var __iterable0__ = props;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var p = __iterable0__ [__index0__];
				try {
					if (p ['name'] == py_name) {
						return p;
					}
				}
				catch (__except0__) {
					if (isinstance (__except0__, KeyError)) {
						return null;
					}
					else {
						throw __except0__;
					}
				}
			}
		};
		var create_context = function (value) {
			return list ([dict ({'name': '__context', 'value': value})]);
		};
		var ce = create_element;
		var cp = create_prop;
		var cjs = function (props, children) {
			return ce ('js', props, children);
		};
		var progn = function (content) {
			return call_anonymous (def_func ('f', '', content));
		};
		var call_anonymous = function (value) {
			var props = list ([cp ('before', '('), cp ('after', ')()')]);
			var children = (py_typeof (value) === str ? value : list ([value]));
			return cjs (props, children);
		};
		var instruction = function (value) {
			var props = list ([cp ('before', '('.format ()), cp ('after', ');')]);
			var children = (py_typeof (value) === str ? value : list ([value]));
			return cjs (props, children);
		};
		var log = function (value) {
			var props = list ([cp ('before', 'console.log('), cp ('after', ')')]);
			var children = value;
			return instruction (cjs (props, children));
		};
		var block = function (value) {
			var props = list ([cp ('before', '{'), cp ('after', '}')]);
			var children = (py_typeof (value) === str ? value : list ([value]));
			return cjs (props, children);
		};
		var def_global = function (py_name, value) {
			var props = list ([cp ('before', 'window.{}='.format (py_name)), cp ('after', '')]);
			var children = list ([instruction (value)]);
			return cjs (props, children);
		};
		var def_local = function (py_name, value) {
			var props = list ([cp ('before', 'let {}='.format (py_name)), cp ('after', '')]);
			var children = list ([instruction (value)]);
			return cjs (props, children);
		};
		var assign = function (py_name, value) {
			var props = list ([cp ('before', '{}='.format (py_name)), cp ('after', '')]);
			var children = list ([instruction (value)]);
			return cjs (props, children);
		};
		var def_func = function (py_name, py_arguments, children) {
			var props = list ([cp ('before', ('function(' + py_arguments) + ') {'), cp ('after', '}')]);
			return cjs (props, children);
		};
		var If = function (condition, children) {
			var props = list ([cp ('before', ('if(' + condition) + ') {'), cp ('after', '}')]);
			return cjs (props, children);
		};
		var Return = function (children) {
			var props = list ([cp ('before', 'return '), cp ('after', '')]);
			return cjs (props, list ([instruction (children)]));
		};
		var op = function (operation, operand, operee) {
			var props = list ([cp ('before', '({} {} '.format (operand, operation)), cp ('after', '{})'.format (operee))]);
			var children = '';
			return cjs (props, children);
		};
		var i = tuple ([instruction (op ('+', '1', '2'))]);
		var content = list ([def_local ('x', "document.getElementById('mySelect').value"), assign ("document.getElementById('demo').innerHTML", op ('+', "'You selected: '", 'x'))]);
		var ast = def_local ('a', '1');
		var ast = call_anonymous (def_func ('f', '', content));
		var js = render_js_element (ast);
		var Div = function (props, children) {
			var children = children || list ([]);
			return ce ('div', props, children);
		};
		var Script = function (string) {
			if (typeof string == 'undefined' || (string != null && string .hasOwnProperty ("__kwargtrans__"))) {;
				var string = '';
			};
			return ce ('script', list ([]), string);
		};
		var ScriptBefore = function (children, script_text) {
			var children = children || list ([]);
			var children = list ([Script (script_text)]) + children;
			return Div (list ([]), children);
		};
		var Grid = function (children) {
			var children = children || list ([]);
			var props = list ([cp ('class', 'mdc-layout-grid__inner')]);
			return Div (props, children);
		};
		var Row = function (children) {
			var children = children || list ([]);
			var props = list ([cp ('class', 'mdc-layout-grid__inner')]);
			return Div (props, children);
		};
		var Cell = function (children) {
			var children = children || list ([]);
			var props = list ([cp ('class', 'mdc-layout-grid__cell')]);
			return Div (props, children);
		};
		var Errors = function () {
			var props = list ([]);
			var children = '\n    errors go here\n    ';
			return Div (props, children);
		};
		var Form = function (children) {
			var props = list ([cp ('class', 'mdc-layout-grid__cell')]);
			var errors = Errors ();
			children.append (errors);
			return ce ('form', props, children);
		};
		var Field = function (children) {
			var children = children || list ([]);
			var props = list ([cp ('class', 'mdc-layout-field')]);
			return Div (props, children);
		};
		var Input = function (value, subscribe_store_change) {
			var update_label_value = function () {
				var content = list ([def_local ('x', 'document.getElementById(`myInput`).value'), log ('`hey` + x'), instruction ('window.todoStore.name=x')]);
				var ast = call_anonymous (def_func ('f', '', content));
				var js = render_js_element (ast);
				return js;
			};
			subscribe_store_change (list ([log ('`killer`'), log ('`keydown`'), instruction ('window.todoStore.name === `foo` ? document.getElementById(`demo`).innerHTML = "you won" : document.getElementById(`demo`).innerHTML = ""')]));
			var props = list ([cp ('type', 'text'), cp ('onkeyup', update_label_value ()), cp ('id', 'myInput'), cp ('value', value)]);
			return ce ('input', props, list ([]));
		};
		var Checkbox = function (is_checked) {
			var props = list ([cp ('class', 'mdc-checkbox__native-control'), cp ('type', 'checkbox'), cp ('id', '{{ id }}'), cp ((is_checked ? 'checked' : ''), '')]);
			return ce ('input', props, list ([]));
		};
		var Label = function (py_name) {
			var c = function (context) {
				var props = list ([]);
				return ce ('label', props, (context ['label'] + ' ') + py_name);
			};
			return c;
		};
		var CheckboxField = function (isChecked) {
			var c = function (context) {
				var children = list ([]);
				var props = list ([cp ('class', 'mdc-form-field')]);
				children.append (Div (list ([cp ('class', 'mdc-checkbox')]), list ([Checkbox (isChecked), Div (list ([cp ('class', 'mdc-checkbox-background')]), list ([])), Label ('Checkbox'), Label (context ['label'])])));
				return Div (props, children);
			};
			return c;
		};
		var create_store = function (store_name, on_store_change) {
			var onchange_cb = store_name + '_cb';
			var code = list ([def_global (onchange_cb, def_func ('f', 'obj, prop', on_store_change)), def_global (store_name, ('new Proxy({}, { set: (obj, prop, value) => {obj[prop]=value;window.' + onchange_cb) + '(obj, prop); return true } })')]);
			var ast = progn (code);
			var js = render_js_element (ast);
			return js;
		};
		var FormSchema = function (value) {
			var store = 'todoStore';
			var store_change_func_content = list ([log ('obj[prop]')]);
			var update_label_value = function () {
				var content = list ([def_local ('x', "document.getElementById('myInput').value"), log ('x'), assign ("document.getElementById('demo').innerHTML", op ('+', "'You selected: '", 'x'))]);
				var ast = progn (content);
				var js = render_js_element (ast);
				return js;
			};
			var get_on_store_change = function () {
				return store_change_func_content;
			};
			var get_js = function () {
				return create_store (store, get_on_store_change ());
			};
			var subscribe_store_change = function (content) {
				store_change_func_content += content;
			};
			var render = function () {
				return ScriptBefore (list ([Form (list ([Cell (list ([Input ('username', subscribe_store_change), Div (list ([create_prop ('style', 'height: 5rem')]), 'If you type <strong>foo</strong> in the textbox and unfocus, your secret message will appear !!'), Div (list ([create_prop ('id', 'demo'), create_prop ('style', 'color: red')]), '')]))]))]), get_js ());
			};
			return render ();
		};
		__pragma__ ('<all>')
			__all__.Cell = Cell;
			__all__.Checkbox = Checkbox;
			__all__.CheckboxField = CheckboxField;
			__all__.Div = Div;
			__all__.Errors = Errors;
			__all__.Field = Field;
			__all__.Form = Form;
			__all__.FormSchema = FormSchema;
			__all__.Grid = Grid;
			__all__.If = If;
			__all__.Input = Input;
			__all__.Label = Label;
			__all__.Return = Return;
			__all__.Row = Row;
			__all__.Script = Script;
			__all__.ScriptBefore = ScriptBefore;
			__all__.__name__ = __name__;
			__all__.assign = assign;
			__all__.ast = ast;
			__all__.block = block;
			__all__.call_anonymous = call_anonymous;
			__all__.ce = ce;
			__all__.cjs = cjs;
			__all__.content = content;
			__all__.context_middleware = context_middleware;
			__all__.cp = cp;
			__all__.create_context = create_context;
			__all__.create_element = create_element;
			__all__.create_prop = create_prop;
			__all__.create_store = create_store;
			__all__.def_func = def_func;
			__all__.def_global = def_global;
			__all__.def_local = def_local;
			__all__.default_middleware = default_middleware;
			__all__.get_prop = get_prop;
			__all__.i = i;
			__all__.instruction = instruction;
			__all__.js = js;
			__all__.log = log;
			__all__.op = op;
			__all__.progn = progn;
			__all__.render_ast = render_ast;
			__all__.render_element = render_element;
			__all__.render_html = render_html;
			__all__.render_js = render_js;
			__all__.render_js_element = render_js_element;
		__pragma__ ('</all>')
	}) ();
