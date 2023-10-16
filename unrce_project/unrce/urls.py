from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Home and landing page
    path('', views.home, name='initial-landing'),

    # Contact page
    path('contact/', views.contact, name='contact'),

    # Expression of interest page
    path('eoi/', views.add_interest, name='eoi'),

    # User authentication paths
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='unrce/login.html', success_url='profile'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Favicon redirect
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),

    # Profile and user-related paths
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('users_list/', views.users_list, name='users_list'),
    path('change-group/<int:user_id>/', views.change_group, name='change_group'),
    path('download_users_csv/', views.download_users_csv, name='download_users_csv'),

    # Report-related paths
    path('report_list/', views.report_list, name='report_list'),
    path('create_report/', views.create_report, name='create_report'),
    path('report_edit/<int:report_id>/', views.report_edit, name='report_edit'),
    path('report/delete/<int:id>/', views.report_delete, name='report_delete'),
    path('report_details/<int:report_id>/', views.report_details, name='report_details'),
    path('browse_reports/', views.browse_reports, name='browse_reports'),
    path('report_review/', views.report_review, name='report_review'),
    path('approve_report/<int:report_id>/', views.approve_report, name='approve_report'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('download_reports/', views.download_reports, name='download_reports'),

    # Membership-related paths
    path('membership_request/', views.membership_request, name='membership_request'),
    path('membership_review/', views.membership_review, name='membership_review'),
    path('approve_membership/<int:account_id>/', views.approve_membership, name='approve_membership'),
]

# Add media URL in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
