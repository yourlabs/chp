from phtml.mdc import Grid, Row, Cell
from phtml.django.mdc import Form, Field

from django import forms

from .models import Post


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

    class Meta:
        model = Post
        exclude = []
