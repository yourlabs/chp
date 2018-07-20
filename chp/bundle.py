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


class ChpTreeWalk(TreeWalk):
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
            print('Passing on', astor.to_source(self.cur_node))
            return
        print(with_attribute, '->', global_name)
        self.replace(ast.Name(id=global_name, ctx=ast.Load()))

    def post_Name(self):
        if self.cur_node.id in self.imports:
            self.cur_node.id = '___' + self.imports[self.cur_node.id].replace('.', '__')


def generate(path):
    with open(path, 'r') as f:
        script = f.read()
    sys.path.append(os.path.dirname(path))
    parsed = ast.parse(script)
    tree = ChpTreeWalk()
    tree.walk(parsed)
    source = [astor.to_source(parsed)]
    for i in set(tree.imports.values()):
        print(i)
        imp.importlib.import_module(i)
        import ipdb; ipdb.set_trace()
    return '\n'.join(source)
