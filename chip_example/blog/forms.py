from django import forms

from .models import Post
from . import chip
from . import pyreact
from django.utils.safestring import mark_safe

def FormSchema(is_checked):
    return chip.Form([
                chip.Row([
                    chip.Input('username'),
                    chip.CheckboxField(is_checked),
                ])
            ])


class PostForm(forms.ModelForm):
    def render(self):
        is_checked = 'checked' # self.checked
        Form = FormSchema(is_checked)

        html = pyreact.render_element(Form)

        return mark_safe(html)

    class Meta:
        model = Post
        exclude = []
