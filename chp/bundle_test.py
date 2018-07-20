import ast
import pytest
import random
import string
import shutil
import os

import chp
from chp import bundle


tests_path = os.path.join(
    os.path.dirname(__file__),
    'tests',
)
if os.path.exists(tests_path):
    shutil.rmtree(tests_path)


def test_Dependency_path_is_None_for_safe_module():
    assert not bundle.Dependency('math').path


@pytest.mark.parametrize('fixture', ['a', 'a.b', 'a.*'])
def test_Dependency_path_for_module_name(fixture, s):
    s('a', 'b=2')
    result = bundle.Dependency(f'{s.module}.{fixture}').path
    assert result == os.path.join(f'{s.path}/a.py')


def test_Dependency_dependencies(s):
    s('entry', f'import {s.module}.a')
    s('a', 'b=2')
    result = bundle.Dependency(f'{s.module}.entry').dependencies
    assert result.names == [f'{s.module}.a']


def test_Dependencies_factory_path(s):
    s('entry', f'import {s.module}.a')
    s('a', 'b = 2')
    result = bundle.Dependencies.factory(f'{s.path}/entry.py')
    assert result.names == [f'{s.module}.a']


def test_Dependencies_recursive(s):
    s('entry', f'import {s.module}.a')
    s('a', f'from {s.module}.b import *'),
    s('b', 'import math')
    result = bundle.Dependency(f'{s.module}.entry').dependencies
    assert result.names == [
        f'{s.module}.a',
        f'{s.module}.b',
    ]


def test_Dependencies_reorder(s):
    s('entry', f'import {s.module}.b; import {s.module}.a')
    s('a', f'import {s.module}.c')
    s('b', f'import {s.module}.c; import {s.module}.a')
    s('c', 'import math')
    result = bundle.Dependency(f'{s.module}.entry').dependencies
    assert result.names == [
        f'{s.module}.b',
        f'{s.module}.a',
        f'{s.module}.c',
    ]


@pytest.mark.parametrize('code,expected', [
    ('a.b', '{}__a__b'),
    ('a.b()', '{}__a__b()'),
    ('a.b.c', '{}__a__b.c'),
])
def test_globalize_imports_from_attribute(code, expected, s):
    s('entry', 'from {module} import a; ' + code)
    tree = bundle.GlobalizeImports.from_path(f'{s.path}/entry.py')
    assert tree.to_source() == expected.format(s.globalized)


def test_get_attribute_name():
    expr = ast.parse('chp.tests.a').body[0].value
    assert bundle.get_attribute_name(expr) == 'chp.tests.a'


@pytest.mark.parametrize('code,expected', [
    ('{module}.a.b', '{}__a__b'),
    ('{module}.a.b()', '{}__a__b()'),
    ('{module}.a.b.c', '{}__a__b.c'),
])
def test_globalize_imports_attribute(code, expected, s):
    s('entry', 'import {module}.a; ' + code)
    tree = bundle.GlobalizeImports.from_path(f'{s.path}/entry.py')
    assert tree.to_source() == expected.format(s.globalized)


@pytest.mark.parametrize('code,expected', [
    ('{module}.a.b', '{}__a__b'),
    ('{module}.a.b()', '{}__a__b()'),
    ('{module}.a.b.c', '{}__a__b.c'),
])
def test_globalize_imports_as_attribute(code, expected, s):
    s('entry', 'import {module}.a; ' + code)
    tree = bundle.GlobalizeImports.from_path(f'{s.path}/entry.py')
    assert tree.to_source() == expected.format(s.globalized)


def test_globalize_imports_star(s):
    s('entry', f'from {s.module}.a import *; foo')
    s('a', 'foo = 1')
    tree = bundle.GlobalizeImports.from_path(f'{s.path}/entry.py')
    assert tree.to_source() == f'{s.globalized}__a__foo'


@pytest.mark.parametrize('code', [
    'lambda foo: foo',
    'lambda foo=None: foo',
])
def test_resist_shadow_import_lambda(code, s):
    s(
        'entry',
        f'from {s.module}.a import *',
        'foo',
        code,
        'foo'
    )
    s('a', 'foo = 1')
    tree = bundle.GlobalizeImports.from_path(f'{s.path}/entry.py')
    assert tree.to_source() == '\n'.join([
        f'{s.globalized}__a__foo',
        code,
        f'{s.globalized}__a__foo',
    ])


@pytest.mark.parametrize('code', [
    'def bar(foo):',
    'def bar(foo=None):',
])
def test_resist_shadow_import_func(code, s):
    s('entry',
        f'from {s.module}.a import *',
        'foo',
        f'{code} return foo',
        'foo',
    )
    s('a', 'foo = 1')
    tree = bundle.GlobalizeImports.from_path(f'{s.path}/entry.py')
    assert tree.to_source() == f'''
{s.globalized}__a__foo


{code}
    return foo


{s.globalized}__a__foo
'''.strip()


@pytest.fixture
def s():
    s = Scenario()
    return s


class Scenario:
    def __init__(self):
        self.name = ''.join(random.choices(string.ascii_letters, k=8))
        self.path = os.path.join(
            tests_path,
            self.name
        )
        self.module = f'chp.tests.{self.name}'
        self.entry_module = f'{self.module}.entry'
        self.entry_path = f'{self.path}/entry.py'
        self.globalized = '___' + self.module.replace('.', '__')
        os.makedirs(self.path)

    def __call__(self, name, *contents):
        """Write a submodule with the given name and content."""
        path = os.path.join(self.path, f'{name}.py')
        content = '\n'.join([c.format(**self.__dict__) for c in contents])
        with open(path, 'w+') as f:
            f.write(content)
