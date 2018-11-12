from django.urls.base import reverse_lazy
from django.views import generic

from .forms import PostForm
from .models import Post


class PostCreateView(generic.CreateView):
    form_class = PostForm
    model = Post

    def get_initial(self):
        initial = super(PostCreateView, self).get_initial()
        initial.update({
            'checkbox': True,
            'text': 'Initial value',
            'media': Post.VHS,
            })
        return initial


class PostUpdateView(generic.UpdateView):
    form_class = PostForm
    model = Post


"""
class PostListView(generic.ListView):
    model = Post


class PostDetailView(generic.DetailView):
    form_class = PostForm
    model = Post
    # template_name_suffix = "_form"


class PostDeleteView(generic.DeleteView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy("post_list")
"""
