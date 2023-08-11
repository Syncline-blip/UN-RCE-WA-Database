from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='unrce-landing'),
    path('project/', views.projects, name='unrce-project'),
]

