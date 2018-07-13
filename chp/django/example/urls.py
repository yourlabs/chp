from django.contrib import admin
from django.views import generic
from django.urls import include, path

urlpatterns = [
    path('', generic.RedirectView.as_view(url='/blog/post/create')),
    path('blog/', include('chp.django.example.blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
]
