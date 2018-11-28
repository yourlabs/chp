import pytest
import re

from chp.django.example.blog.forms import PostForm
from chp.mdc.django.factory import Factory as MdcField
from chp.pyreact import render_element


pytestmark = pytest.mark.django_db


@pytest.fixture(scope="module")
def postform():
    return PostForm(initial={
        "checkbox": True,
        "text": "Initial value",
        "date": "2018-10-03",
        "media": "vinyl",
        # "foreignkey": ""  # will require database setup fixture
        })


@pytest.fixture(scope="module")
def postform_html(postform):
    # TODO: Django doesn't handle scoped database access in pytest
    # https://github.com/pytest-dev/pytest-django/issues/514
    # https://github.com/django-nose/django-nose/issues/276#issuecomment-412623604
    # return postform.render()
    pass

def test_render(postform):
    """Regression test."""

    regex = """
<div class="mdc-layout-grid" chp-id="[0-9]+">
<div class="mdc-layout-grid__inner" chp-id="[0-9]+">
<div class="mdc-layout-grid__cell--span-12" chp-id="[0-9]+">
<form id="form-chp" chp-id="[0-9]+">
<input type="hidden" name="csrfmiddlewaretoken" value="REQUEST NOT AVAILABLE IN CONTEXT" chp-id="[0-9]+" />
<div style="display: flex;" chp-id="[0-9]+">
<div class="mdc-form-field mdc-form-field--align-end" data-mdc-auto-init="MDCFormField" chp-id="[0-9]+">
<div class="mdc-checkbox" data-mdc-auto-init="MDCCheckbox" chp-id="[0-9]+"><input name="checkbox" id="id_checkbox" checked class="mdc-checkbox__native-control" type="checkbox" chp-id="[0-9]+" />
<div class="mdc-checkbox__background" chp-id="[0-9]+"></div></div><label for="id_checkbox" chp-id="[0-9]+">This is my checkbox:</label></div>
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField" chp-id="[0-9]+"><input name="text" value="Initial value" maxlength="[0-9]+" required id="id_text" class="mdc-text-field__input" type="text" chp-id="[0-9]+" />
<label for="id_text" class="mdc-floating-label" chp-id="[0-9]+">Input Label:</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div></div>
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField" chp-id="[0-9]+"><input name="date" value="2018-10-03" required id="id_date" class="mdc-text-field__input" type="date" chp-id="[0-9]+" />
<label for="id_date" class="mdc-floating-label" chp-id="[0-9]+">Type = date:</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div></div>
<div class="mdc-select" data-mdc-auto-init="MDCSelect" chp-id="[0-9]+">
<select name="media" required id="id_media" class="mdc-select__native-control" chp-id="[0-9]+">
<option value="" disabled chp-id="[0-9]+"></option><optgroup label="Audio" chp-id="[0-9]+"><option value="vinyl" selected chp-id="[0-9]+">Vinyl</option><option value="cd" chp-id="[0-9]+">CD</option><option value="mp3" chp-id="[0-9]+">MP3</option></optgroup><optgroup label="Video" chp-id="[0-9]+"><option value="vhs" chp-id="[0-9]+">VHS tape</option><option value="dvd" chp-id="[0-9]+">DVD</option><option value="blu-ray" chp-id="[0-9]+">Blu-ray</option></optgroup>
</select>
<label for="id_media" class="mdc-floating-label" chp-id="[0-9]+">Media:</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div></div>
<div class="mdc-select" data-mdc-auto-init="MDCSelect" chp-id="[0-9]+">
<select name="foreignkey" required id="id_foreignkey" class="mdc-select__native-control" chp-id="[0-9]+">
<option value="" selected disabled chp-id="[0-9]+"></option>
</select>
<label for="id_foreignkey" class="mdc-floating-label" chp-id="[0-9]+">Foreignkey:</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div></div></div>
<div style="display: grid;" chp-id="[0-9]+">
<div class="mdc-button" data-mdc-auto-init="None" chp-id="[0-9]+"><button form="form-chp" type="submit" chp-id="[0-9]+">Submit</button></div></div>
</form></div></div></div>
"""
    regex = regex.replace("\n", "")
    regexc = re.compile(regex)
    assert re.match(regexc, postform.render()) is not None


def test_render_checkbox(postform):
    fld = MdcField.render(postform["checkbox"])
    html = render_element(fld)
    test_str = """
<div class="mdc-form-field mdc-form-field--align-end" data-mdc-auto-init="MDCFormField">
 <div class="mdc-checkbox" data-mdc-auto-init="MDCCheckbox">
  <input name="checkbox" id="id_checkbox" checked class="mdc-checkbox__native-control" type="checkbox" />
  <div class="mdc-checkbox__background"></div>
 </div>
 <label for="id_checkbox">This is my checkbox:</label>
</div>
"""
    test_str = re.sub("\n\s*", "", test_str)
    assert html == test_str


def test_render_text(postform):
    fld = MdcField.render(postform["text"])
    html = render_element(fld)
    test_str = """
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField">
 <input name="text" value="Initial value" maxlength="200" required id="id_text" class="mdc-text-field__input" type="text" />
 <label for="id_text" class="mdc-floating-label">Input Label:</label>
 <div class="mdc-line-ripple"></div>
</div>
"""
    test_str = re.sub("\n\s*", "", test_str)
    assert html == test_str


def test_render_date(postform):
    fld = MdcField.render(postform["date"])
    html = render_element(fld)
    test_str = """
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField">
 <input name="date" value="2018-10-03" required id="id_date" class="mdc-text-field__input" type="date" />
 <label for="id_date" class="mdc-floating-label">Type = date:</label>
 <div class="mdc-line-ripple"></div>
</div>
"""
    test_str = re.sub("\n\s*", "", test_str)
    assert html == test_str


def test_render_media(postform):
    fld = MdcField.render(postform["media"])
    html = render_element(fld)
    test_str = """
<div class="mdc-select" data-mdc-auto-init="MDCSelect">
 <select name="media" required id="id_media" class="mdc-select__native-control">
  <option value="" disabled></option>
  <optgroup label="Audio">
   <option value="vinyl" selected>Vinyl</option>
   <option value="cd">CD</option>
   <option value="mp3">MP3</option>
  </optgroup>
  <optgroup label="Video">
   <option value="vhs">VHS tape</option>
   <option value="dvd">DVD</option>
   <option value="blu-ray">Blu-ray</option>
  </optgroup>
 </select>
 <label for="id_media" class="mdc-floating-label">Media:</label>
 <div class="mdc-line-ripple"></div>
</div>
"""
    test_str = re.sub("\n\s*", "", test_str)
    assert html == test_str


# TODO: needs a fixture to create database entries
def test_render_foreignkey(postform):
    fld = MdcField.render(postform["foreignkey"])
    html = render_element(fld)
    test_str = """
<div class="mdc-select" data-mdc-auto-init="MDCSelect">
 <select name="foreignkey" required id="id_foreignkey" class="mdc-select__native-control">
  <option value="" selected disabled></option>
 </select>
 <label for="id_foreignkey" class="mdc-floating-label">Foreignkey:</label>
 <div class="mdc-line-ripple"></div>
</div>
"""
    test_str = re.sub("\n\s*", "", test_str)
    assert html == test_str
