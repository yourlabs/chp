import pytest
import os
import shutil

import chp
from chp import bundle


JS_PATH = os.path.join(os.path.dirname(__file__), 'js.py')
TEST_PATH = os.path.join(os.path.dirname(__file__), 'tests', 'test_module')
TEST_MODULE = 'chp.tests.test_module'
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
    assert list(result) == ['chp.tests.test_module.a']


def test_Dependencies_factory_path():
    scenario(f'import {TEST_MODULE}.a', a='b = 2')
    dependencies = bundle.Dependencies.factory(ENTRY_PATH)
    assert list(dependencies) == ['chp.tests.test_module.a']


def test_Dependencies_recursive():
    scenario(
        f'import {TEST_MODULE}.a',
        a=f'from {TEST_MODULE}.b import *',
        b=f'import math',
    )
    result = bundle.Dependency(f'{TEST_MODULE}.entry').dependencies
    assert list(result) == [
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
    assert list(result) == [
        'chp.tests.test_module.b',
        'chp.tests.test_module.a',
        'chp.tests.test_module.c',
    ]


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
