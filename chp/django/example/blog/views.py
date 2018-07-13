from django.views import generic

from .forms import PostForm
from .models import Post


class PostCreateView(generic.CreateView):
    form_class = PostForm
    model = Post
