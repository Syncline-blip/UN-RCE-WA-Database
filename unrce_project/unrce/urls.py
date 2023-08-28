from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.home, name='home_landing'),
    path('project/', views.projects, name='unrce-project'),
    path('add/', views.add_report, name='add_report'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/edit/<int:pk>/', views.report_edit, name='report_edit'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='unrce/login.html', success_url='profile'), name='login'),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit_report/', views.edit_reporting, name='edit_report'),
    path('report_details/', views.reportDetails, name='report_details'),
]

