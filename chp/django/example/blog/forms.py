from datetime import date

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from chp.components import *  #noqa
from chp.pyreact import (
    context_middleware, inject_ids, render_element
)
# from chp.store import (create_store, Inject_ast_into_DOM, render_app)
from chp.django.components import Csrf
from chp.mdc.components import *  # noqa
from chp.mdc.django.factory import Factory

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"
        labels = {
            "checkbox": _("This is my checkbox"),
            "text": _("Input Label"),
            "date": _("Type = date"),
        }
        help_texts = {
            "text": _(
                "Enter 'Error' to raise a general form error on submit"),
            "date": _(
                "Enter a date earlier than today"),
            "media": _(
                "Select a media format from the dropdown list"),
        }

    def clean_date(self):
        data = self.cleaned_data["date"]
        max_date = date.today()
        if data >= max_date:
            raise forms.ValidationError(
                _("Date must be earlier than %(max_date)s"),
                code="max_date",
                params={"max_date": max_date.strftime("%d/%m/%Y")}
            )
        return data

    def clean(self):
        if self.cleaned_data.get("text", "").lower() == "error":
            raise forms.ValidationError(
                _("General form error."),
                code="invalid_form"
            )

    def FormSchema(self, *args, **kwargs):

        def render(self, *args, **kwargs):

            def mdc(f):
                return Factory.render(self[f])

            def errors(f):
                return Factory.errors(self[f])

            def help_text(f):
                return Factory.help_text(self[f])

            def non_field_errors(self):
                return Factory.non_field_errors(self)

            form = (
                Grid([], [
                Row([], [
                Cell([], [
                Form([
                        cp("id", "form-chp"),
                        cp("method", "POST"),
                    ],
                    [
                        Csrf(),
                        Flex([],
                             [
                             non_field_errors(self),
                             mdc("checkbox"),
                             errors("checkbox"),
                             help_text("checkbox"),
                             mdc("text"),
                             errors("text"),
                             help_text("text"),
                             mdc("date"),
                             errors("date"),
                             help_text("date"),
                             mdc("media"),
                             errors("media"),
                             help_text("media"),
                             mdc("foreignkey"),
                             errors("foreignkey"),
                             help_text("foreignkey"),
                             ], {"display": "grid"}),
                        Flex([],
                             [
                             SubmitButton([cp("form", "form-chp")]),
                             ]),
                    ])
                ], {"span": 6})  # Cell
                ])  # Row
                ])  # Grid
            )  # noqa

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
