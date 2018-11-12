import pytest
import re

from chp.django.example.blog.forms import PostForm


pytestmark = pytest.mark.django_db


def test_render():
    """Regression test."""

    # <form action="/blog/post/create" method="POST" class="mdc-layout-grid__cell" chp-id="[0-9]+">
    # </form>
    # <option value="grains" chp-id="[0-9]+">Bread, Cereal, Rice, and Pasta</option><option value="vegetables" chp-id="[0-9]+">Vegetables</option><option value="fruit" chp-id="[0-9]+">Fruit</option>
    # <option value="1" chp-id="[0-9]+">johnk</option>
    # <option value="2" chp-id="[0-9]+">jpic</option>
    # <option value="3" chp-id="[0-9]+">vindarel</option>


    regex = """
<div style="display: flex;" chp-id="[0-9]+">
<div class="mdc-form-field mdc-form-field--align-end" data-mdc-auto-init="MDCFormField" chp-id="[0-9]+">
<div class="mdc-checkbox" data-mdc-auto-init="MDCCheckbox" chp-id="[0-9]+"><input name="checkbox" id="id_checkbox" class="mdc-checkbox__native-control" type="checkbox" chp-id="[0-9]+" />
<div class="mdc-checkbox__background" chp-id="[0-9]+"></div></div><label for="id_checkbox" chp-id="[0-9]+">This is my checkbox:</label></div>
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField" chp-id="[0-9]+"><input name="text" maxlength="200" required id="id_text" class="mdc-text-field__input" type="text" chp-id="[0-9]+" />
<label for="id_text" class="mdc-floating-label" chp-id="[0-9]+">Input Label:</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div></div>
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField" chp-id="[0-9]+"><input name="date" required id="id_date" class="mdc-text-field__input" type="date" chp-id="[0-9]+" />
<label for="id_date" class="mdc-floating-label" chp-id="[0-9]+">Type = date:</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div></div>
<div class="mdc-select" data-mdc-auto-init="MDCSelect" chp-id="[0-9]+"><select name="media" required id="id_media" class="mdc-select__native-control" chp-id="[0-9]+">
<option value="" selected disabled chp-id="[0-9]+"></option><optgroup label="Audio" chp-id="[0-9]+"><option value="vinyl" chp-id="[0-9]+">Vinyl</option><option value="cd" chp-id="[0-9]+">CD</option><option value="mp3" chp-id="[0-9]+">MP3</option></optgroup><optgroup label="Video" chp-id="[0-9]+"><option value="vhs" chp-id="[0-9]+">VHS tape</option><option value="dvd" chp-id="[0-9]+">DVD</option><option value="blu-ray" chp-id="[0-9]+">Blu-ray</option></optgroup>
</select><label for="id_media" class="mdc-floating-label" chp-id="[0-9]+">Media:</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div></div>
<div class="mdc-select" data-mdc-auto-init="MDCSelect" chp-id="[0-9]+"><select name="foreignkey" required id="id_foreignkey" class="mdc-select__native-control" chp-id="[0-9]+">
<option value="" selected disabled chp-id="[0-9]+"></option>
</select>
<label for="id_foreignkey" class="mdc-floating-label" chp-id="[0-9]+">Foreignkey:</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div></div></div>
"""
    regex = regex.replace("\n", "")
    regexc = re.compile(regex)
    result = PostForm().render()
    assert re.match(regexc, result) is not None


def test_render_checkbox():
    test_value = True
    f = PostForm(initial={"checkbox": test_value})
    assert "checked" in f.render()


def test_render_text():
    test_value = "Initial value"
    f = PostForm(initial={"text": test_value})
    assert test_value in f.render()


def test_render_date():
    test_value = "2018-10-03"
    f = PostForm(initial={"date": test_value})
    assert test_value in f.render()


def test_render_media():
    test_value = "vinyl"
    f = PostForm(initial={"media": test_value})
    assert test_value in f.render()


# TODO: needs a fixture to create a foreign key
def test_render_foreignkey():
    test_value = ""
    f = PostForm(initial={"foreignkey": test_value})
    assert test_value in f.render()
