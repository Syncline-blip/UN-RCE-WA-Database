from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.home, name='home_landing'),
    path('project/', views.projects, name='unrce-project'),
    path('add/', views.add_report, name='add_report'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/edit/<int:pk>/', views.report_edit, name='report_edit'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='unrce/login_temp.html'), name='login'),
]
