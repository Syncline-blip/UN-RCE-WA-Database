from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home_landing'),
    path('project/', views.projects, name='unrce-project'),
    path('create_report/', views.create_report, name='create_report'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/edit/<int:pk>/', views.report_edit, name='report_edit'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', LoginView.as_view(template_name='unrce/login_temp.html'), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)