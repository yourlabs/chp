import json

from chp import chp

from django.utils.safestring import mark_safe
from django.views import generic

from .components import FormSchema


class TodosView(generic.TemplateView):
    template_name = 'todos.html'

    def body(self):
        is_checked = {
            "name": "hello",
        }
        ctx={
            "label": "Labelling:",
            "password": "bar"
        }
        store = {
            "name": "this is my first store !!",
            "todos": [
                {
                    "name": "hello",
                    "id": "0",
                },
                {
                    "name": "todo number secondo !!",
                    "id": "1",
                },
            ]
        }
        ast = FormSchema(store, json.dumps(store))
        form = chp.inject_ids(ast)
        app = chp.Inject_ast_into_DOM(form, json.dumps(form))
        html = chp.render_element(app, chp.context_middleware(ctx))
        return mark_safe(html)
