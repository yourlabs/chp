from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from chp import chp
from chp.components import *
from chp.pyreact import (
    context_middleware, inject_ids, render_element
)
from chp.store import (create_store, Inject_ast_into_DOM, render_app)

from chp.mdc.components import *
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

            form = Form([
                cp('action', reverse('blog:post_create')),
                cp('method', "POST"),
                ],
                [
                Flex([],
                     [
                        MdcField.render(self["checkbox"]),
                        MdcField.render(self["text"]),
                        MdcField.render(self["date"]),
                        SelectField([
                            # cp("required", "required"),
                            cp("name", "foreignkey"),
                            cp("id", "id_foreignkey"),
                            cp("required", True),
                            ], [
                            Option([
                                cp("value", ""),
                                ]
                            ),
                            Option([
                                cp("value", "grains"),
                                ],
                                "Bread, Cereal, Rice, and Pasta"
                            ),
                            Option([
                                cp("value", "vegetables"),
                                ],
                                "Vegetables"
                            ),
                            Option([
                                cp("value", "fruit"),
                                ],
                                "Fruit"
                            ),
                            ],
                            {"label": "Pick a Food Group",
                             }
                        )
                    ],
                ),
                ])

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
