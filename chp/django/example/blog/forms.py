from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from chp import chp
from chp.components import *  #noqa
from chp.pyreact import (
    context_middleware, inject_ids, render_element
)
from chp.store import (create_store, Inject_ast_into_DOM, render_app)
# from chp.django.components import *  #noqa
from chp.mdc.components import *  # noqa
from chp.mdc.django.factory import Factory as MdcField

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"
        labels = {
            'checkbox': _("This is my checkbox"),
            'text': _("Input Label"),
            'date': _("Type = date"),
        }

    def FormSchema(self, *args, **kwargs):

        def render(self, *args, **kwargs):

            form = (
                # Form([
                # cp('id', "form-chp"),
                # ],
                # [
                # Csrf(),
                Flex([],
                     [
                        MdcField.render(self["checkbox"]),
                        MdcField.render(self["text"]),
                        MdcField.render(self["date"]),
                        MdcField.render(self["media"]),
                        MdcField.render(self["foreignkey"]),
                    ],
                )
                # ,
                # ])
                )

            return form

        return render(self)

    def render(self):

        ctx = {}

        ast = self.FormSchema()
        form = inject_ids(ast, context_middleware(ctx))
#         app = Inject_ast_into_DOM(form, json.dumps(form))
#         html = render_element(app, context_middleware(ctx))
        html = render_element(form, context_middleware(ctx))

        return mark_safe(html)
