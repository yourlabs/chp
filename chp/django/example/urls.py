from django.contrib import admin
from django.views import generic
from django.urls import include, path

urlpatterns = [
    path('', generic.RedirectView.as_view(url='/todos')),
    path('blog/', include('chp.django.example.blog.urls', namespace='blog')),
    path('todos/', include('chp.django.example.todos.urls')),
    path('admin/', admin.site.urls),
]
