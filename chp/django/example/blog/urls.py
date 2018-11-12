from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('post/create',
         views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/',
         views.PostUpdateView.as_view(), name='post_update'),
    # path('post/list',
    #      views.PostListView.as_view(), name='post_list'),
    # path('post/detail/<int:pk>/',
    #      views.PostDetailView.as_view(), name='post_detail'),
    # path('post/delete/<int:pk>/',
    #      views.PostDeleteView.as_view(), name='post_delete'),
]
