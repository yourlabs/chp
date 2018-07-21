from django.urls import path

from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.TodosView.as_view(), name='todos'),
]
