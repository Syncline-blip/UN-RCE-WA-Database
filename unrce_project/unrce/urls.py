from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='initial-landing'),
    path('eoi/', views.add_interest, name='eoi'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='unrce/login.html', success_url='profile'), name='login'),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('report_list/', views.report_list, name='report_list'),
    path('report_review/', views.report_review, name='report_review'),
    path('report_details/', views.reportDetails, name='report_details'),
    path('create_report/', views.create_report, name='create_report'),
    path('redirect/', views.must_be_signed_in, name='redirect'),
    path('report_edit/<int:report_id>/', views.report_edit, name='report_edit'),
    path('report_details/<int:report_id>/', views.report_details, name='report_details'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('users_list/', views.users_list, name='users_list'),
    path('eoi_review/', views.eoi_review, name='eoi_review'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)