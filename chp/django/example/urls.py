from django.conf import settings
from django.contrib import admin
from django.urls import include, path, reverse_lazy, re_path
from django.views import generic

urlpatterns = [
    path('', generic.RedirectView.as_view(url=reverse_lazy('blog:default'))),
    path('blog/', include('chp.django.example.blog.urls',
                          namespace='blog')),
    path('todos/', include('chp.django.example.todos.urls',
                           namespace='todos')),
    path('admin/', admin.site.urls),
]

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
