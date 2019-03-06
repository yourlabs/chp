import pytest
import re

from django.core.exceptions import ValidationError
from django.test import TestCase

from chp.components import Div
from chp.django.example.blog.forms import PostForm
from chp.mdc.django.factory import Factory as MdcField
from chp.pyreact import render_element

pytestmark = pytest.mark.django_db
user_name = "rofl"


@pytest.fixture(scope="module")
def postform():
    return PostForm(initial={
        "checkbox": True,
        "text": "Initial value",
        "date": "2018-10-03",
        "media": "vinyl",
        "foreignkey": user_name
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

    regex = r"""
<div class="mdc-layout-grid" chp-id="\d+">
<div class="mdc-layout-grid__inner" chp-id="\d+">
<div class="mdc-layout-grid__cell--span-6" chp-id="\d+">
<form id="form-chp" method="POST" chp-id="\d+">
<input type="hidden" name="csrfmiddlewaretoken" value="\w+" chp-id="\d+" />
<div style="display: grid;" chp-id="\d+">
<div class="mdc-form-field mdc-form-field--align-left" data-mdc-auto-init="MDCFormField" chp-id="\d+">
<div class="mdc-checkbox" data-mdc-auto-init="MDCCheckbox" chp-id="\d+"><input name="checkbox" id="id_checkbox" checked class="mdc-checkbox__native-control" type="checkbox" chp-id="\d+" />
<div class="mdc-checkbox__background" chp-id="\d+"></div></div><label for="id_checkbox" chp-id="\d+">This is my checkbox:</label></div>
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField" chp-id="\d+"><input name="text" value="Initial value" maxlength="\d+" required id="id_text" class="mdc-text-field__input" type="text" chp-id="\d+" />
<label for="id_text" class="mdc-floating-label" chp-id="\d+">Input Label:</label>
<div class="mdc-line-ripple" chp-id="\d+"></div></div>
<div class="mdc-text-field-helper-line" chp-id="\d+"><div class="mdc-text-field-helper-text mdc-text-field-helper-text--persistent" id="text-helper-text" chp-id="\d+">Enter &#39;Error&#39; to raise a general form error on submit</div></div>
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField" chp-id="\d+"><input name="date" value="\d+-\d+-\d+" required id="id_date" class="mdc-text-field__input" type="date" chp-id="\d+" />
<label for="id_date" class="mdc-floating-label" chp-id="\d+">Type = date:</label>
<div class="mdc-line-ripple" chp-id="\d+"></div></div>
<div class="mdc-text-field-helper-line" chp-id="\d+"><div class="mdc-text-field-helper-text mdc-text-field-helper-text--persistent" id="date-helper-text" chp-id="\d+">Enter a date earlier than today</div></div>
<div class="mdc-select" data-mdc-auto-init="MDCSelect" chp-id="\d+">
<select name="media" required id="id_media" class="mdc-select__native-control" chp-id="\d+">
<option value="" disabled chp-id="\d+"></option><optgroup label="Audio" chp-id="\d+"><option value="vinyl" selected chp-id="\d+">Vinyl</option><option value="cd" chp-id="\d+">CD</option><option value="mp3" chp-id="\d+">MP3</option></optgroup><optgroup label="Video" chp-id="\d+"><option value="vhs" chp-id="\d+">VHS tape</option><option value="dvd" chp-id="\d+">DVD</option><option value="blu-ray" chp-id="\d+">Blu-ray</option></optgroup>
</select>
<label for="id_media" class="mdc-floating-label" chp-id="\d+">Media:</label>
<div class="mdc-line-ripple" chp-id="\d+"></div></div>
<div class="mdc-text-field-helper-line" chp-id="\d+"><div class="mdc-text-field-helper-text mdc-text-field-helper-text--persistent" id="media-helper-text" chp-id="\d+">Select a media format from the dropdown list</div></div>
<div class="mdc-select" data-mdc-auto-init="MDCSelect" chp-id="\d+">
<select name="foreignkey" required id="id_foreignkey" class="mdc-select__native-control" chp-id="\d+">
<option value="" disabled chp-id="\d+"></option>
</select>
<label for="id_foreignkey" class="mdc-floating-label" chp-id="\d+">Foreignkey:</label>
<div class="mdc-line-ripple" chp-id="\d+"></div></div></div>
<div style="display: flex;" chp-id="\d+">
<button form="form-chp" class="mdc-button" type="submit" chp-id="\d+">Submit</button></div>
</form></div></div></div>
"""  # noqa
    regex = regex.replace("\n", "")
    regexc = re.compile(regex)
    assert re.match(regexc, postform.render()) is not None


def test_render_checkbox(postform):
    fld = MdcField.render(postform["checkbox"])
    html = render_element(fld)
    test_str = """
<div class="mdc-form-field mdc-form-field--align-left" data-mdc-auto-init="MDCFormField">
 <div class="mdc-checkbox" data-mdc-auto-init="MDCCheckbox">
  <input name="checkbox" id="id_checkbox" checked class="mdc-checkbox__native-control" type="checkbox" />
  <div class="mdc-checkbox__background"></div>
 </div>
 <label for="id_checkbox">This is my checkbox:</label>
</div>
"""  # noqa
    test_str = re.sub(r"\n\s*", "", test_str)
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
"""  # noqa
    test_str = re.sub(r"\n\s*", "", test_str)
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
"""  # noqa
    test_str = re.sub(r"\n\s*", "", test_str)
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
"""  # noqa
    test_str = re.sub(r"\n\s*", "", test_str)
    assert html == test_str


# TODO: needs a fixture to create database entries
def test_render_foreignkey(postform):
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
    user_model.objects.create(username=user_name)

    fld = MdcField.render(postform["foreignkey"])
    html = render_element(fld)
    test_str = f"""
<div class="mdc-select" data-mdc-auto-init="MDCSelect">
 <select name="foreignkey" required id="id_foreignkey" class="mdc-select__native-control">
  <option value="" disabled></option>
  <option value="1">{user_name}</option>
 </select>
 <label for="id_foreignkey" class="mdc-floating-label">Foreignkey:</label>
 <div class="mdc-line-ripple"></div>
</div>
"""  # noqa
    test_str = re.sub(r"\n\s*", "", test_str)
    assert html == test_str 


def test_render_form_errors():
    # Receive form with initial values
    # POST form to create view
    # Compare form.errors with MdcField(form.errors)
    postform = PostForm({})  # should yield an invalid form
    test_field = "date"
    postform.is_valid()  # ignore result
    invalid_msg = postform[test_field].field.error_messages["invalid"]
    postform.add_error(test_field,
                       ValidationError(invalid_msg, code="invalid"))
    err_msg = "<br />".join(postform.errors[test_field])
    ast_fld = MdcField.render(postform[test_field])
    ast_err = MdcField.errors(postform[test_field])
    ast = Div([], [ast_fld, ast_err])
    html = render_element(ast)

    test_str = f"""
<div>
<div class="mdc-text-field mdc-text-field--invalid" data-mdc-auto-init="MDCTextField">
 <input name="date" required id="id_date" class="mdc-text-field__input" type="date" />
 <label for="id_date" class="mdc-floating-label">Type = date:</label>
 <div class="mdc-line-ripple"></div>
</div>
<div class="mdc-text-field-helper-line"><div class="mdc-text-field-helper-text--validation-msg mdc-text-field-helper-text mdc-text-field-helper-text--persistent" class="mdc-text-field-helper-text--validation-msg" id="{test_field}-helper-text">{err_msg}</div></div>
</div>
"""  # noqa
    test_str = re.sub(r"\n\s*", "", test_str)
    assert html == test_str


class FormTest(TestCase):
    def test_uses_post_form_template(self):
        response = self.client.get("/blog/post/create")
        self.assertTemplateUsed(response, "blog/post_form.html")

