import re

from chp.django.example.blog.forms import PostForm


def test_render():
    regex = '''
<form action="/blog/post/create" method="POST" class="mdc-layout-grid__cell" chp-id="[0-9]+">
<div style="display: flex;" chp-id="[0-9]+">
<div class="mdc-form-field mdc-form-field--align-end" data-mdc-auto-init="MDCFormField" chp-id="[0-9]+">
<div class="mdc-checkbox" data-mdc-auto-init="MDCCheckbox" chp-id="[0-9]+">
<input type="checkbox" id="id_checkbox" class="mdc-checkbox__native-control" type="checkbox" chp-id="[0-9]+" />
<div class="mdc-checkbox__background" chp-id="[0-9]+"></div>
</div>
<label for="id_checkbox" chp-id="[0-9]+">This is my checkbox:</label>
</div>
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField" chp-id="[0-9]+">
<input type="text" id="id_text" maxlength="200" class="mdc-text-field__input" chp-id="[0-9]+" />
<label for="id_text" class="mdc-floating-label" chp-id="[0-9]+">Input Label</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div>
</div>
<div class="mdc-text-field" data-mdc-auto-init="MDCTextField" chp-id="[0-9]+">
<input type="date" id="id_date" class="mdc-text-field__input" chp-id="[0-9]+" />
<label for="id_date" class="mdc-floating-label" chp-id="[0-9]+">Type = date</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div>
</div>
<div class="mdc-select" data-mdc-auto-init="MDCSelect" chp-id="[0-9]+">
<select id="id_foreignkey" class="mdc-select__native-control" chp-id="[0-9]+">
<option value selected="selected" chp-id="[0-9]+"></option><option value="grains" chp-id="[0-9]+">Bread, Cereal, Rice, and Pasta</option><option value="vegetables" chp-id="[0-9]+">Vegetables</option><option value="fruit" chp-id="[0-9]+">Fruit</option>
</select>
<label for="id_foreignkey" class="mdc-floating-label" chp-id="[0-9]+">Pick a Food Group</label>
<div class="mdc-line-ripple" chp-id="[0-9]+"></div>
</div></div>
</form>
'''
    regex = regex.replace("\n", "")
    regexc = re.compile(regex)
    assert re.match(regexc, PostForm().render()) is not None
