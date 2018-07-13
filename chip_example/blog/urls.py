from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('post/create', views.PostCreateView.as_view(), name='post_create'),
]
