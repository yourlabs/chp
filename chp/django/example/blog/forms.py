from django import forms

from . import chp
from . import Form

from .models import Post
from django.utils.safestring import mark_safe


class PostForm(forms.ModelForm):
    def render(self):
        ctx={
            "name": "JPic",
            "password": "Aaroon et Mia"
        }
        ast = Form.Form()
        html = chp.render_element(ast, chp.context_middleware(ctx))
        return mark_safe(html)

    class Meta:
        model = Post
        exclude = []
