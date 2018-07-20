import ast
import pytest
import os
import shutil

import chp
from chp import bundle


JS_PATH = os.path.join(os.path.dirname(__file__), 'js.py')
TEST_PATH = os.path.join(os.path.dirname(__file__), 'tests', 'test_module')
TEST_MODULE = 'chp.tests.test_module'
TEST_MODULE_GLOBALIZE = '___' + TEST_MODULE.replace('.', '__')
ENTRY_PATH = os.path.join(TEST_PATH, 'entry.py')


def test_Dependency_path_is_None_for_safe_module():
    assert not bundle.Dependency('math').path


@pytest.mark.parametrize('fixture', ['a', 'a.b', 'a.*'])
def test_Dependency_path_for_module_name(fixture):
    scenario(a='b = 2')
    result = bundle.Dependency(f'{TEST_MODULE}.{fixture}').path
    assert result == os.path.join(TEST_PATH, 'a.py')


def test_Dependency_dependencies():
    scenario(f'import {TEST_MODULE}.a', a='b = 2')
    result = bundle.Dependency(f'{TEST_MODULE}.entry').dependencies
    assert result.names == ['chp.tests.test_module.a']


def test_Dependencies_factory_path():
    scenario(f'import {TEST_MODULE}.a', a='b = 2')
    result = bundle.Dependencies.factory(ENTRY_PATH)
    assert result.names == ['chp.tests.test_module.a']


def test_Dependencies_recursive():
    scenario(
        f'import {TEST_MODULE}.a',
        a=f'from {TEST_MODULE}.b import *',
        b=f'import math',
    )
    result = bundle.Dependency(f'{TEST_MODULE}.entry').dependencies
    assert result.names == [
        'chp.tests.test_module.a',
        'chp.tests.test_module.b',
    ]


def test_Dependencies_reorder():
    scenario(
        f'import {TEST_MODULE}.b; import {TEST_MODULE}.a',
        a=f'import {TEST_MODULE}.c',
        b=f'import {TEST_MODULE}.c; import {TEST_MODULE}.a',
        c=f'import math',
    )
    result = bundle.Dependency(f'{TEST_MODULE}.entry').dependencies
    assert result.names == [
        'chp.tests.test_module.b',
        'chp.tests.test_module.a',
        'chp.tests.test_module.c',
    ]


@pytest.mark.parametrize('code,expected', [
    ('a.b', f'{TEST_MODULE_GLOBALIZE}__a__b'),
    ('a.b()', f'{TEST_MODULE_GLOBALIZE}__a__b()'),
    ('a.b.c', f'{TEST_MODULE_GLOBALIZE}__a__b.c'),
])
def test_globalize_imports_from_attribute(code, expected):
    scenario(
        f'from {TEST_MODULE} import a; {code}',
    )
    tree = bundle.GlobalizeImports.from_path(ENTRY_PATH)
    assert tree.to_source() == expected


def test_get_attribute_name():
    expr = ast.parse('chp.tests.a').body[0].value
    assert bundle.get_attribute_name(expr) == 'chp.tests.a'


@pytest.mark.parametrize('code,expected', [
    (f'{TEST_MODULE}.a.b', f'{TEST_MODULE_GLOBALIZE}__a__b'),
])
def test_globalize_imports_attribute(code, expected):
    scenario(
        f'import {TEST_MODULE}.a; {code}',
    )
    tree = bundle.GlobalizeImports.from_path(ENTRY_PATH)
    assert tree.to_source() == expected


def test_generate():
    return
    scenario(
        f'''
from {TEST_MODULE}.a import A
class x(A):
    def echo(self, A):
        print(A)
        '''.strip(),
        a=f'''
class A:
    pass
        '''.strip(),
    )
    result = bundle.generate(ENTRY_PATH)
    print(result)
    assert result == '''
class ___a_A:
    pass

class x(___a_A):
    pass
'''.strip()


def scenario(entry=None, **files):
    if os.path.exists(TEST_PATH):
        shutil.rmtree(TEST_PATH)
    os.makedirs(TEST_PATH)

    if entry:
        with open(ENTRY_PATH, 'w+') as f:
            f.write(entry)

    for name, content in files.items():
        with open(os.path.join(TEST_PATH, f'{name}.py'), 'w+') as f:
            f.write(content)

'''

def test_noop():
    path = scenario(
        'a = 1',
    )
    result = bundle.generate(path)
    assert result == 'a = 1'


def test_simple_import():
    path = scenario(
        'from a import foo',
        a='foo = 2',
    )
    result = bundle.generate(path)
    assert result == 'foo = 2'
'''
