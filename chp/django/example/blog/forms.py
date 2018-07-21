from django import forms
from django.utils.safestring import mark_safe

from chp import chp

from .models import Post

class PostForm(forms.ModelForm):
    def render(self):
        import json
        ast = FormSchema(store, json.dumps(store))
        form = chp.pyreact.inject_ids(ast)
        app = chp.Inject_ast_into_DOM(form, json.dumps(form))
        html = chp.render_element(app, chp_build.context_middleware(ctx))
        print(html)
        print(form)
        return mark_safe(html)

    class Meta:
        model = Post
        exclude = []
