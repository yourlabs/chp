import chp
from . import todos

from django import forms

from .models import Post
from django.utils.safestring import mark_safe

def FormSchema(is_checked):

    return chp.Form([
        chp.Row([
            chp.Input('username'),
            chp.CheckboxField(is_checked),
            chp.Div([chp.create_prop("id", "demo")], "yo")
        ])
    ])



class PostForm(forms.ModelForm):
    def render(self):
        is_checked = 'checked' # self.checked
        ctx={
            "label": "Labelling:",
            "password": "bar"
        }
        Form = todos.FormSchema(is_checked)
        html = chp.render_element(Form, chp.context_middleware(ctx))
        return mark_safe(html)

    class Meta:
        model = Post
        exclude = []
