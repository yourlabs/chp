import chp

from django import forms

from .models import Post
from django.utils.safestring import mark_safe

def FormSchema(is_checked):
    return chp.Form([
        chp.Row([
            chp.Input('username'),
            chp.CheckboxField(is_checked),
        ])
    ])


class PostForm(forms.ModelForm):
    def render(self):
        is_checked = 'checked' # self.checked
        Form = FormSchema(is_checked)
        html = chp.render_element(Form)
        return mark_safe(html)

    class Meta:
        model = Post
        exclude = []
