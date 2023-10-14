from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='initial-landing'),
    path('contact/', views.contact, name='contact'),
    path('eoi/', views.add_interest, name='eoi'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='unrce/login.html', success_url='profile'), name='login'),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('report_list/', views.report_list, name='report_list'),
    path('report_review/', views.report_review, name='report_review'),
    path('report_details/', views.report_details, name='report_details'),
    path('create_report/', views.create_report, name='create_report'),
    path('redirect/', views.must_be_signed_in, name='redirect'),
    path('report_edit/<int:report_id>/', views.report_edit, name='report_edit'),
    path('report_details/<int:report_id>/', views.report_details, name='report_details'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('users_list/', views.users_list, name='users_list'),
    path('eoi_review/', views.eoi_review, name='eoi_review'),
    path('membership_request/', views.membership_request, name='membership_request'),
    path('browse_reports/', views.browse_reports, name='browse_reports'),
    path('approve_report/<int:report_id>/', views.approve_report, name='approve_report'),
    path('change-group/<int:user_id>/', views.change_group, name='change_group'),
    path('userprofile/', views.user_profile, name='user_profile'),
    path('membership_review/', views.membership_review, name='membership_review'),
    path('approve_membership/<int:account_id>/', views.approve_membership, name='approve_membership'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
