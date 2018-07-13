from phtml.mdc import Grid, Row, Cell
from phtml.django.mdc import Form, Field

from django import forms

from .models import Post
import chip


class PostForm(forms.ModelForm):
    _phtml = Grid(Form(
        Row(
            Cell(Field('title')),
        ),
        Row(
            Cell(Field('author')),
            Cell(Field('publish_datetime')),
        )
    ))

    def render(self):
        return chip.Form([
                chip.Row([
                    chip.Input('username'),
                    chip.CheckboxField('password'),
                ])
            ])

    class Meta:
        model = Post
        exclude = []
