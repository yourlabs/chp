from django.views import generic

from .forms import PostForm
from .models import Post


class PostCreateView(generic.CreateView):
    form_class = PostForm
    model = Post

    def get_initial(self):
        initial = super(PostCreateView, self).get_initial()
        initial.update({'checkbox': True,
                        'text': 'Initial value',
                        })
        return initial
