"""
Let's generate a single script from a python script with imports.

From the script, generate a list of imports that :gq:m\
"""
import ast
import astor
from astor.tree_walk import TreeWalk
import imp
import os
import sys


IMPORT_SAFE = (
    'math',
    'random',
)


def get_attribute_name(node):
    result = []
    while getattr(node, 'value', None):
        attr = getattr(node, 'attr', None)

        if node.attr:
            result.append(node.attr)
            node = node.value
    result.append(node.id)
    return '.'.join(reversed(result))


def module_file(name):
    parts = name.split('.')
    mod = None
    while mod is None:
        try:
            mod = imp.importlib.import_module('.'.join(parts))
        except ImportError:
            parts.pop()
    return getattr(mod, '__file__', None)


class TreeWalk(TreeWalk):
    @classmethod
    def from_module(cls, module, **kwargs):
        return cls.from_path(Dependency(module).path, **kwargs)

    @classmethod
    def from_path(cls, path, **kwargs):
        with open(path, 'r') as f:
            content = f.read()
        return cls.from_content(content, **kwargs)

    @classmethod
    def from_content(cls, content, **kwargs):
        return cls.from_ast(ast.parse(content), **kwargs)

    @classmethod
    def from_ast(cls, ast, **kwargs):
        tree = cls()
        tree.ast = ast
        for key, value in kwargs.items():
            setattr(tree, key, value)
        tree.walk(ast)
        return tree

    def to_source(self):
        return astor.to_source(self.ast).strip()


class ImportWalker(TreeWalk):
    def init_imports(self):
        self.imports = Dependencies()

    def init_targets(self):
        self.targets = dict()

    def post_Import(self):
        for name in self.cur_node.names:
            module = name.name
            target = name.asname or name.name
            if module not in self.imports:
                self.imports.append(module)
            self.targets[target] = module

    def post_ImportFrom(self):
        self.imports.append(self.cur_node.module)

        for name in self.cur_node.names:
            target = name.asname or name.name
            if name.name == '*':
                importable = f'{self.cur_node.level*"."}{self.cur_node.module}'
                if self.cur_node.level:
                    raise Exception(
                        f'chp does not support relative imports: {importable}'
                    )
                mod = imp.importlib.import_module(importable)
                for name in mod.__dict__.keys():
                    if name.startswith('__'):
                        continue
                    self.targets[name] = f'{importable}.{name}'
            else:
                self.targets[target] = f'{self.cur_node.module}.{name.name}'


class Path(str):
    @property
    def dependencies(self):
        if not self:
            return Dependencies()

        tree = ImportWalker.from_path(self)
        results = Dependencies(tree.imports)
        for result in tree.imports:
            for sub in result.dependencies:
                results.append(sub)

        return results


class Dependency(object):
    def __init__(self, name, target=None):
        self.target = target or name
        self.name = name

    def __str__(self):
        return self.name

    @property
    def path(self):
        if self.name in IMPORT_SAFE:
            return Path()

        parts = self.name.split('.')
        mod = None
        while mod is None:
            if not parts:
                return Path()

            try:
                mod = imp.importlib.import_module('.'.join(parts))
            except ImportError:
                parts.pop()

        return Path(getattr(mod, '__file__', None))

    @property
    def dependencies(self):
        return self.path.dependencies

    @property
    def globalized(self):
        return '___' + self.name.replace('.', '__')


class Dependencies(list):
    @classmethod
    def factory(cls, path=None):
        with open(path, 'r') as f:
            content = f.read()

        parsed = ast.parse(content)
        tree = ImportWalker()
        tree.walk(parsed)

        instance = cls()
        for i in tree.imports:
            instance.append(i)
        return instance

    @property
    def names(self):
        return [d.name for d in self]

    def index(self, value):
        if not isinstance(value, Dependency):
            value = Dependency(value)
        return self.names.index(value.name)

    def append(self, value):
        if not isinstance(value, Dependency):
            value = Dependency(value)

        if value.name in IMPORT_SAFE:
            return

        try:
            position = self.index(value)
        except ValueError:
            pass
        else:
            self.pop(position)

        return super().append(value)


def dependencies(path, results=None):
    path = os.path.abspath(path)

    if results:
        results.append(path)
    else:
        results = Dependencies([path])

    with open(path, 'r') as f:
        content = f.read()
    parsed = ast.parse(content)

    tree = ImportWalker()
    tree.walk(parsed)
    new_results = []
    for i in tree.imports:
        if i in IMPORT_SAFE:
            continue
        f = module_file(i)
        if f and f.endswith('.py') and f not in results:
            print(f'{path} requires {i} resolving to {f}')
            new_results.append(f)
            results.append(f)

    for result in new_results:
        dependencies(result, results)

    return results


class GlobalizeImports(ImportWalker):
    def delete(self):
        """Delete a node after first checking integrity of node stack."""
        return self.parent.pop(self.parent.index(self.cur_node))

    def post_ImportFrom(self):
        ImportWalker.post_ImportFrom(self)
        self.delete()

    def post_Import(self):
        ImportWalker.post_Import(self)
        self.delete()

    def pre_Attribute(self):
        name = astor.to_source(self.cur_node).strip()
        left = '.'.join(name.split('.')[:-1])
        right = name.split('.')[-1]
        if left in self.targets:
            fixed = f'{self.targets[left]}'.replace('.', '__')
            self.replace(ast.Name(
                f'___{fixed}__{right}',
                ast.Load()
            ))

    def post_Name(self):
        if self.scope and self.cur_node.id in self.scope_args:
            return

        if self.cur_node.id in self.targets:
            self.cur_node.id = '___' + self.targets[self.cur_node.id].replace('.', '__')
            return True

    @property
    def scope(self):
        scopes = ['FunctionDef', 'Lambda']
        i = len(self.nodestack) - 1
        while i:
            node = self.nodestack[i][0]
            if type(node).__name__ in scopes:
                return node
            i -= 1

    @property
    def scope_args(self):
        return [arg.arg for arg in self.scope.args.args]


class GlobalizeDeclares(GlobalizeImports):
    def init_renames(self):
        self.renames = dict()

    def post_Assign(self):
        if self.scope:
            return

        for name in self.cur_node.targets:
            if not hasattr(name, 'id'):
                continue
            if self.scope and name.id in self.scope_args:
                continue
            new_name = f'{self.prefix}__{name.id}'
            self.renames[name.id] = new_name
            name.id = new_name

    def pre_FunctionDef(self):
        if self.scope and self.cur_node.name in self.scope_args:
            return

        new_name = f'{self.prefix}__{self.cur_node.name}'
        self.renames[self.cur_node.name] = new_name
        self.cur_node.name = new_name
    pre_ClassDef = pre_FunctionDef

    def post_Name(self):
        if GlobalizeImports.post_Name(self):
            return

        name = self.cur_node.id
        if name and name in self.renames.keys():
            self.cur_node.id = self.renames[name]
            return True

'''
OLD CODE, remove soon


class GlobalizeImportsTreeWalk(TreeWalk):
    def init_imports(self):
        self.imports = dict()

    def delete(self):
        """Delete a node after first checking integrity of node stack."""
        return self.parent.pop(self.parent.index(self.cur_node))

    def post_ImportFrom(self):
        for name in self.cur_node.names:
            target = name.asname or name.name
            if target == '*':
                importable = f'{self.cur_node.level*"."}{self.cur_node.module}'
                if self.cur_node.level:
                    raise Exception(
                        f'chp does not support relative imports: {importable}'
                    )
                mod = imp.importlib.import_module(importable)
                for name in mod.__dict__.keys():
                    if name.startswith('__'):
                        continue
                    self.imports[name] = f'{importable}.{name}'
            else:
                self.imports[target] = self.cur_node.module
        self.delete()

    def post_Import(self):
        for name in self.cur_node.names:
            module = name.name
            target = name.asname or name.name
            self.imports[target] = module
        self.delete()

    def post_Attribute(self):
        parts = [self.cur_node.attr]
        subject = self.cur_node
        while getattr(subject, 'value', None):
            id = getattr(subject.value, 'id', None)
            attr = getattr(subject.value, 'attr', None)
            parts.insert(0, attr or id)
            subject = subject.value
        with_attribute = '.'.join(parts)
        without_attribute = '.'.join(parts[:-1])
        if with_attribute in self.imports:
            global_name = '___' + self.imports[with_attribute].replace('.', '__')
        elif without_attribute in self.imports:
            global_name = '___' + self.imports[without_attribute].replace('.', '__') + '__' + self.cur_node.attr
        elif self.cur_node.value.id.startswith('___'):
            global_name = '__'.join([self.cur_node.value.id, self.cur_node.attr])
        else:
            return
        self.replace(ast.Name(id=global_name, ctx=ast.Load()))

    def post_Name(self):
        if self.cur_node.id in self.imports:
            self.cur_node.id = '___' + self.imports[self.cur_node.id].replace('.', '__')
            return True


class GlobalizeDeclaresTreeWalk(GlobalizeImportsTreeWalk):
    def init_renames(self):
        self.renames = dict()

    def post_FunctionDef(self):
        new_name = f'{self.prefix}__{self.cur_node.name}'
        self.renames[self.cur_node.name] = new_name
        self.cur_node.name = new_name

    def post_Name(self):
        if GlobalizeImportsTreeWalk.post_Name(self):
            return

        name = self.cur_node.id
        if name and name in self.renames.keys():
            self.cur_node.id = self.renames[name]
            return True


def globalize_imports(path):
    tree = GlobalizeImportsTreeWalk.from_path(path)
    return tree.to_source()


def generate(path):
    with open(path, 'r') as f:
        script = f.read()
    sys.path.append(os.path.dirname(path))
    parsed = ast.parse(script)
    tree = GlobalizeImportsTreeWalk()
    tree.walk(parsed)
    source = [astor.to_source(parsed)]

    for dep in Path(path).dependencies:
        if not dep.path:
            continue

        prefix = '___' + dep.path.replace('.', '__') + '__'
        with open(dep.path, 'r') as f:
            script = f.read()
        parsed = ast.parse(script)
        tree = GlobalizeDeclaresTreeWalk()
        tree.prefix = prefix
        tree.walk(parsed)
        source.append(astor.to_source(parsed))

    return '\n'.join(reversed(source))
'''
