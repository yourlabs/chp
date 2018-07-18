	(function () {
		var math = {};
		var random = {};
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
		var default_middleware = function (el, _props, _children) {
			if (typeof _props == 'undefined' || (_props != null && _props .hasOwnProperty ("__kwargtrans__"))) {;
				var _props = list ([]);
			};
			if (typeof _children == 'undefined' || (_children != null && _children .hasOwnProperty ("__kwargtrans__"))) {;
				var _children = list ([]);
			};
			return el;
		};
		__nest__ (math, '', __init__ (__world__.math));
		__nest__ (random, '', __init__ (__world__.random));
		var diff_asts = function (old, py_new) {
			var patches = list ([]);
			var new_tree = dict ({});
			var old_name = old ['name'];
			var old_props = old ['props'];
			var new_name = py_new ['name'];
			var new_props = py_new ['props'];
			if (old_name != new_name) {
				patches.append (dict ({'type': 'replace-element', 'chp-id': get_prop (old_props, 'chp-id') ['value'], 'html': render_element (py_new)}));
				var new_tree = py_new;
			}
			else {
				var i = 0;
				var props_differ = false;
				if (len (old_props) != len (new_props)) {
					var props_differ = true;
				}
				if (!(props_differ)) {
					while (i < len (new_props)) {
						var c1 = old_props [i] ['name'] != new_props [i] ['name'];
						var c2 = old_props [i] ['value'] != new_props [i] ['value'];
						if (c1 || c2) {
							if (new_props [i] ['name'] != 'children') {
								if (new_props [i] ['name'] != 'chp-id') {
									var props_differ = true;
								}
							}
						}
						i++;
					}
				}
				if (props_differ) {
					var id = get_prop (new_props, 'chp-id');
					id ['value'] = get_prop (old_props, 'chp-id') ['value'];
					patches.append (dict ({'type': 'props', 'chp-id': get_prop (old_props, 'chp-id') ['value'], 'props': new_props}));
					var new_tree = py_new;
					new_tree ['props'] = new_props;
				}
				else {
					var new_tree = old;
				}
			}
			var nc = get_prop (new_props, 'children');
			var oc = get_prop (old_props, 'children');
			var new_children = (nc ? nc ['value'] : list ([]));
			var old_children = (oc ? oc ['value'] : list ([]));
			if (len (new_children) != len (old_children)) {
				var html = '';
				if (py_typeof (new_children) === str) {
					var html = new_children;
				}
				else {
					var new_tree_children = get_prop (new_tree ['props'], 'children');
					new_tree_children ['value'] = list ([]);
					var __iterable0__ = new_children;
					for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
						var c = __iterable0__ [__index0__];
						html += render_element (c);
						new_tree_children ['value'].append (c);
					}
				}
				patches.append (dict ({'type': 'innerHTML', 'chp-id': get_prop (old_props, 'chp-id') ['value'], 'html': html}));
			}
			else {
				var new_tree_children = get_prop (new_tree ['props'], 'children');
				new_tree_children ['value'] = get_prop (py_new ['props'], 'children') ['value'];
				if (py_typeof (new_children) === str) {
					new_tree_children ['value'] = new_children;
				}
				else {
					new_tree_children ['value'] = list ([]);
					var i = 0;
					while (i < len (new_children)) {
						var child_diff = diff_asts (old_children [i], new_children [i]);
						var ps = child_diff [0];
						var __iterable0__ = ps;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var p = __iterable0__ [__index0__];
							patches.append (p);
						}
						i++;
						new_tree_children ['value'].append (child_diff [1]);
					}
				}
			}
			return list ([patches, new_tree]);
		};
		var render_html = function (el, props, child) {
			var py_name = el ['name'];
			var children = '';
			var __iterable0__ = child;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var c = __iterable0__ [__index0__];
				children += c;
			}
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
			return '<{} {}>{}</{}>'.format (py_name, props_str, children, py_name);
		};
		var render_js = function (el, props, child) {
			var py_name = el ['name'];
			var props_str = '';
			var children = '';
			var __iterable0__ = child;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var c = __iterable0__ [__index0__];
				children += c;
			}
			var before = get_prop (props, 'before') ['value'];
			var after = get_prop (props, 'after') ['value'];
			return '{}{}{}'.format (before, children, after);
		};
		var id_middleware = function (ast) {
			var props = ast ['props'];
			props.append (dict ({'name': 'chp-id', 'value': str (math.floor (random.random () * 10000000))}));
			return ast;
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
			var child = list ([]);
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
					child.append (render_ast (c, ast_middleware, render_middleware));
				}
			}
			return render_middleware (ast, props, child);
		};
		var inject_ids = function (ast) {
			return render_ast (ast, id_middleware, default_middleware);
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
			var props = list ([cp ('before', '('), cp ('after', ')();')]);
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
		var Button = function (props, children) {
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
			var script = list ([Script (script_text)]);
			var children = script.append (children);
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
			var children = '\n    ';
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
		var create_store = function (store_name, on_store_change, json_init_state) {
			var onchange_cb = store_name + '_cb';
			var code = list ([def_global (onchange_cb, def_func ('f', 'obj, prop', on_store_change)), def_global (store_name, ((("!window.todoStore ? new Proxy(JSON.parse('" + json_init_state) + "'), { set: (obj, prop, value) => {obj[prop]=value;window.") + onchange_cb) + '(obj, prop); return true } }) : window.todoStore')]);
			var ast = progn (code);
			var js = render_js_element (ast);
			return js;
		};
		var patch_dom = function (patches) {
			var __iterable0__ = patches;
			for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
				var patch = __iterable0__ [__index0__];
				var py_metatype = patch ['type'];
				var chp_id = patch ['chp-id'];
				if (py_metatype == 'props') {
					var props = patch ['props'];
					var __iterable1__ = props;
					for (var __index1__ = 0; __index1__ < len (__iterable1__); __index1__++) {
						var prop = __iterable1__ [__index1__];
						var el = document ['querySelector'] ("[chp-id='{}']".format (chp_id));
						if (prop ['name'] != 'chp-id') {
							el.setAttribute (prop ['name'], prop ['value']);
							if (prop ['name'] == 'value') {
								el ['value'] = prop ['value'];
							}
						}
					}
				}
				else if (py_metatype == 'innerHTML') {
					var el = document ['querySelector'] ("[chp-id='{}']".format (chp_id));
					el.innerHTML = patch ['html'];
				}
			}
		};
		var render_app = function (store_name, store_content_json) {
			return progn (list ([def_local ('old_chp_ast', 'window.chp_ast ? window.chp_ast : JSON.parse(document.querySelector("[chp-id=\'chp-ast\']").innerHTML)'), def_local ('new_chp_ast', "inject_ids(FormSchema(window.{}, '{}'))".format (store_name, store_content_json)), def_local ('[patches, new_ast_from_diff]', 'old_chp_ast ? window.diff_asts(old_chp_ast, new_chp_ast) : false'), def_global ('chp_ast', 'new_ast_from_diff'), progn ('patch_dom(patches)'), progn ("eval(document.querySelector('body script').innerHTML);")]));
		};
		var remove_todo = function (todo_id) {
			var todos = todoStore ['todos'] || list ([]);
			var todos = list (filter ((function __lambda__ (t) {
				return parseFloat (t ['id']) != todo_id;
			}), todos));
			todoStore.todos = todos;
		};
		var update_todo_name = function () {
			var x = document ['getElementById'] ('myInput');
			todoStore ['name'] = x ['value'];
		};
		var add_todo = function (todoStore) {
			var todos = todoStore.todos || list ([]);
			var t = todos.__getslice__ (0, null, 1);
			t.append (dict ({'name': todoStore ['name'], 'id': str (random.random ())}));
			todoStore ['todos'] = t;
			todoStore ['name'] = '';
		};
		var store_updates = dict ({'add_todo': add_todo, 'remove_todo': remove_todo, 'update_todo_name': update_todo_name});
		var SubmitButton = function (py_name, on_click) {
			var props = list ([cp ('onclick', on_click)]);
			return Button (props, py_name);
		};
		var TodoItem = function (py_name, todo_id) {
			var on_click = 'store_updates.remove_todo({})'.format (todo_id);
			var props = list ([cp ('id', todo_id), cp ('style', 'margin: 1rem; min-height: 3rem; background-color: rgba(0, 0, 0, 0.2); border: 2px solid black'), cp ('onclick', on_click)]);
			return Div (props, py_name);
		};
		var Input = function (value) {
			var on_key_up = 'store_updates.update_todo_name()';
			var props = list ([cp ('type', 'text'), cp ('onkeyup', on_key_up), cp ('id', 'myInput'), cp ('value', value)]);
			return ce ('input', props, list ([]));
		};
		var FormSchema = function (store_content, store_content_json) {
			var store_name = 'todoStore';
			var store_change_cb = list ([render_app (store_name, store_content_json)]);
			var add_todos = function () {
				return 'store_updates.add_todo({})'.format (store_name);
			};
			var render = function () {
				var form = Form (list ([Cell (list ([Div (list ([cp ('style', 'display: flex;')]), list ([Input (store_content ['name']), SubmitButton ('Submit', add_todos ())])), Div (list ([create_prop ('style', 'height: 5rem')]), 'If you type <strong>foo</strong> in the textbox and unfocus, your secret message will appear !!'), Div (list ([create_prop ('id', 'demo'), create_prop ('style', (store_content ['name'] == 'foo' ? 'color: red' : 'color: green'))]), 'what color am I ?')]))]));
				var todos = list ([]);
				var __iterable0__ = store_content ['todos'];
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var t = __iterable0__ [__index0__];
					todos.append (TodoItem (t ['name'], t ['id']));
				}
				return Div (list ([]), list ([Script (create_store (store_name, store_change_cb, store_content_json)), form, Div (list ([]), todos)]));
			};
			return render ();
		};
		var AST = function (json_ast) {
			var children = json_ast;
			var props = list ([cp ('style', 'display: none'), cp ('chp-id', 'chp-ast')]);
			return Div (props, children);
		};
		var injectAstIntoDOM = function (ast) {
			window.chp_ast = ast;
		};
		var Inject_ast_into_DOM = function (app, json_ast) {
			var children = list ([app, AST (json_ast), Script ('window.chp_ast = JSON.parse(document.querySelector("[chp-id=\'chp-ast\']").innerHTML)')]);
			return Div (list ([]), children);
		};
		__pragma__ ('<use>' +
			'math' +
			'random' +
		'</use>')
		__pragma__ ('<all>')
			__all__.AST = AST;
			__all__.Button = Button;
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
			__all__.Inject_ast_into_DOM = Inject_ast_into_DOM;
			__all__.Input = Input;
			__all__.Label = Label;
			__all__.Return = Return;
			__all__.Row = Row;
			__all__.Script = Script;
			__all__.ScriptBefore = ScriptBefore;
			__all__.SubmitButton = SubmitButton;
			__all__.TodoItem = TodoItem;
			__all__.__name__ = __name__;
			__all__.add_todo = add_todo;
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
			__all__.diff_asts = diff_asts;
			__all__.get_prop = get_prop;
			__all__.i = i;
			__all__.id_middleware = id_middleware;
			__all__.injectAstIntoDOM = injectAstIntoDOM;
			__all__.inject_ids = inject_ids;
			__all__.instruction = instruction;
			__all__.js = js;
			__all__.log = log;
			__all__.op = op;
			__all__.patch_dom = patch_dom;
			__all__.progn = progn;
			__all__.remove_todo = remove_todo;
			__all__.render_app = render_app;
			__all__.render_ast = render_ast;
			__all__.render_element = render_element;
			__all__.render_html = render_html;
			__all__.render_js = render_js;
			__all__.render_js_element = render_js_element;
			__all__.store_updates = store_updates;
			__all__.update_todo_name = update_todo_name;
		__pragma__ ('</all>')
	}) ();
