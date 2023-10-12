from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ReportForm, RegistrationForm, InterestForm, ReportImagesForm, ReportFilesForm, OrganizationInlineFormSet
from .models import Report, Account, ReportImages, Expression_of_interest, ReportFiles,themes_esd, priority_action_areas, AUDIENCE_CHOICES, DELIVERY_CHOICES, FREQUENCY_CHOICES
from django.http import HttpResponseServerError, JsonResponse  
import os, json
import pandas as pd
import logging
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.urls import reverse_lazy


logger = logging.getLogger(__name__)
# sample data, not to be used, just for testing
project = [
    {
        'author': 'JOHN JOHN',
        'project': 'PROJECT LIVE',
        'project_code': 22341
    }
]
def home(request):
    return render(request, 'unrce/initial-landing.html')

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_member(user):
    return user.groups.filter(name='Member').exists() or is_admin(user)

def is_visitor(user):
    return user.groups.filter(name='Visitor').exists() or is_member(user) or is_admin(user)

@login_required
@user_passes_test(is_member,login_url=reverse_lazy('initial-landing'))
def create_report(request): 
    try:
    
        if request.method == 'POST':
            report_form = ReportForm(request.POST)
            images_form = ReportImagesForm(request.POST, request.FILES)
            files_form = ReportFilesForm(request.POST, request.FILES)
            organization_formset = OrganizationInlineFormSet(request.POST)
            images = request.FILES.getlist('image')
            files = request.FILES.getlist('file')

            direct_sdgs = []
            indirect_sdgs = []
            for i in range(1, 18):
                option = request.POST.get(f'sdg_option_{i}')
                if option == 'direct':
                    direct_sdgs.append(str(i))
                elif option == 'indirect':
                    indirect_sdgs.append(str(i))

            direct_esd = []
            indirect_esd = []
            for theme in themes_esd:
                option = request.POST.get(f'esd_theme_option_{theme}')
                if option == 'direct':
                    direct_esd.append(theme)
                elif option == 'indirect':
                    indirect_esd.append(theme)

            direct_priority = []
            indirect_priority = []
            for area in priority_action_areas:
                option = request.POST.get(f'esd_priority_option_{area}')
                if option == 'direct':
                    direct_priority.append(area)
                elif option == 'indirect':
                    indirect_priority.append(area)

            if report_form.is_valid() and organization_formset.is_valid():
                report = report_form.save(commit=False)
                report.author = request.user
                report.direct_sdgs = direct_sdgs  
                report.indirect_sdgs = indirect_sdgs 
                report.direct_esd_themes = direct_esd  
                report.indirect_esd_themes = indirect_esd
                report.direct_priority_areas = direct_priority
                report.indirect_priority_areas = indirect_priority
                report.save()

                organization_formset = OrganizationInlineFormSet(request.POST, instance=report)
                if organization_formset.is_valid():
                    organization_formset.save()
                report_form.save_m2m()  

                if images:
                    for image in images:
                        ReportImages.objects.create(
                            report=report,
                            image=image
                        )

                if files:
                    for file in files:
                        ReportFiles.objects.create(
                            report=report,
                            file=file
                        )

                return redirect('report_list')
            else:
                for form in [report_form, images_form, files_form, organization_formset]:
                    if not form.is_valid():
                        logger.error(f'{form.__class__.__name__} errors: {form.errors}')

        else:
            report_form = ReportForm()
            images_form = ReportImagesForm()
            files_form= ReportFilesForm()
            report = Report()
            organization_formset = OrganizationInlineFormSet(instance=report)

        sdg_list = [str(i) for i in range(1, 18)]
        context = {
            'report_form': report_form,
            'organization_formset': organization_formset,
            'images_form': images_form,
            'files_form': files_form,
            'sdg_list': sdg_list,
            'themes_esd': themes_esd,
            'priority_action_areas': priority_action_areas,
            'all_users': User.objects.all(),
        }

        return render(request, 'unrce/create_report.html', context)

    except Exception as e:
        # Logging the error for debugging
        logger.error(f'Error creating report: {str(e)}')
        return redirect('report_list')


def add_interest(request):
    """
    Handles the creation of a new Expression of Interest. This view initializes and validates
    the InterestForm. Upon validation, it associates the current user as the author, saves the form,
    and redirects to the initial landing page.
    """
    if request.method == 'POST':
        Interest_Form = InterestForm(request.POST)

        if Interest_Form.is_valid():
            interest = Interest_Form.save(commit=False)
            interest.author = request.user
            interest.save()
            return redirect('initial-landing')
    else:
        report_form = InterestForm()

    return render(request, 'unrce/eoi.html', {'form': InterestForm})


def contact(request):
    return render(request, 'unrce/contact.html')


@login_required
@user_passes_test(is_member,login_url=reverse_lazy('initial-landing'))
def report_list(request):
    """
    Lists all the Report objects authored by the currently logged-in user.
    Fetches and filters the Report objects by the current user and renders them in 'unrce/report_list.html'.
    """
    reports = Report.objects.filter(author=request.user)
    return render(request, 'unrce/report_list.html', {'reports': reports})


def browse_reports(request):
    """
    Lists all the approved Report objects.
    Fetches and filters the Report objects by approved attribute being True 
    and renders them in 'unrce/approved_reports_list.html'.
    """
    filters = {
        'status': request.GET.get('statusFilter'),
        'region': request.GET.get('regionFilter'),
        'frequency': request.GET.get('frequencyFilter'),
        'approved': True
    }

    audience_filter = request.GET.getlist('audienceFilter')
    if audience_filter:
        filters['audience__overlap'] = audience_filter

    filters = {k: v for k, v in filters.items() if v}
    approved_reports = Report.objects.filter(**filters)

    sdg_filter = request.GET.getlist('sdgFilter')
    if sdg_filter:
        q_objects = Q()

        # Create Q objects for each SDG filter selected by the user
        for sdg in sdg_filter:
            q_objects |= Q(direct_sdgs__contains=[sdg]) | Q(indirect_sdgs__contains=[sdg])

        # Filter the queryset with the OR'ed Q objects
        approved_reports = approved_reports.filter(q_objects)

    context = {
        'sdgs': range(1, 18),
        'reports': approved_reports
    }

    return render(request, 'unrce/browse_reports.html', context)

@login_required
@user_passes_test(is_member,login_url=reverse_lazy('initial-landing'))
def delete_image(request, image_id):
    """
    Allows users to delete images they have uploaded to reports
    """
    image = get_object_or_404(ReportImages, id=image_id)
    report = image.report
    if image.report.author == request.user:
        image.delete()
    return redirect('report_edit', report_id=report.id)


@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def users_list(request):
    query = request.GET.get('q') 

    if query:
        # Filter users by search term while looking into username, first name, last name, and email
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)|
            Q(account__organization__icontains=query)
        ).prefetch_related('groups', 'account')
    else:
        # If there's no search term, get all users
        users = User.objects.all().prefetch_related('groups', 'account')

    context = {
        'users': users,
        'all_groups': Group.objects.all()
    }
    return render(request, 'unrce/users_list.html', context)

@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def report_review(request):
    """
    Lists all the Report objects available in the system, without filtering by author.
    Fetches all the Report objects and renders them in 'unrce/report_review.html'.
    """
    reports = Report.objects.filter()
    return render(request, 'unrce/report_review.html', {'reports': reports})

def report_details(request, report_id):
    """
    Lists the entire report for review, this is accessed from the report_review list of all reports
    """
    report = get_object_or_404(Report, id=report_id)
    report_form = ReportForm(instance=report)
    existing_images = ReportImages.objects.filter(report=report)
    
    context = {
        'form': report_form, 
        'existing_images': existing_images,
        'report': report
    }
    return render(request, 'unrce/report_details.html', context)

def eoi_review(request):
    """
    Lists all the Report objects available in the system, without filtering by author.
    Fetches all the Report objects and renders them in 'unrce/report_review.html'.
    """
    eois = Expression_of_interest.objects.filter()
    return render(request, 'unrce/eoi_review.html', {'eois': eois})



@login_required
@user_passes_test(is_member,login_url=reverse_lazy('initial-landing'))
def report_edit(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    # Ensure the request.user is the author of the report or has permission
    if report.author != request.user:
        return redirect('report_list')

    try:
        if request.method == 'POST':
            report_form = ReportForm(request.POST, instance=report)
            images_form = ReportImagesForm(request.POST, request.FILES)
            files_form = ReportFilesForm(request.POST, request.FILES)
            organization_formset = OrganizationInlineFormSet(request.POST, instance=report)
            images = request.FILES.getlist('image')
            files = request.FILES.getlist('file')

            if report_form.is_valid() and organization_formset.is_valid():
                report = report_form.save(commit=False)  # Do not save immediately

                # Capture the radio button selections for SDGs, ESD Themes, and Priority Areas
                direct_sdgs = []
                indirect_sdgs = []
                for i in range(1, 18):
                    option = request.POST.get(f'sdg_option_{i}')
                    if option == 'direct':
                        direct_sdgs.append(str(i))
                    elif option == 'indirect':
                        indirect_sdgs.append(str(i))

                direct_esd = []
                indirect_esd = []
                for theme in themes_esd:
                    option = request.POST.get(f'esd_theme_option_{theme}')
                    if option == 'direct':
                        direct_esd.append(theme)
                    elif option == 'indirect':
                        indirect_esd.append(theme)

                direct_priority = []
                indirect_priority = []
                for area in priority_action_areas:
                    option = request.POST.get(f'esd_priority_option_{area}')
                    if option == 'direct':
                        direct_priority.append(area)
                    elif option == 'indirect':
                        indirect_priority.append(area)

                report.direct_sdgs = direct_sdgs
                report.indirect_sdgs = indirect_sdgs
                report.direct_esd_themes = direct_esd
                report.indirect_esd_themes = indirect_esd
                report.direct_priority_areas = direct_priority
                report.indirect_priority_areas = indirect_priority
                
                report.save()  # Now save after updating the above fields

                organization_formset = OrganizationInlineFormSet(request.POST, instance=report)
                if organization_formset.is_valid():
                    organization_formset.save()
                report_form.save_m2m()  


                # Removing existing images/files and add new ones
                for image in images:
                    ReportImages.objects.create(report=report, image=image)

                for file in files:
                    ReportFiles.objects.create(report=report, file=file)

                return redirect('report_list')
            else:
                for form in [report_form, images_form, files_form, organization_formset]:
                    if not form.is_valid():
                        logger.error(f'{form.__class__.__name__} errors: {form.errors}')

        else:
            report_form = ReportForm(instance=report)
            images_form = ReportImagesForm()
            files_form = ReportFilesForm()
            organization_formset = OrganizationInlineFormSet(instance=report)

        sdg_list = [str(i) for i in range(1, 18)]
        context = {
            'report': report,
            'report_form': report_form,
            'organization_formset': organization_formset,
            'images_form': images_form,
            'files_form': files_form,
            'sdg_list': sdg_list,
            'themes_esd': themes_esd,
            'priority_action_areas': priority_action_areas,
            'existing_images': ReportImages.objects.filter(report=report),
            'existing_files': ReportFiles.objects.filter(report=report)
        }

        return render(request, 'unrce/report_edit.html', context)

    except Exception as e:
        # Logging the error for debugging
        logger.error(f'Error editing report: {str(e)}')
        return redirect('report_list')


def register(request):
    try:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                logging.debug("Form is valid")
                user = form.save()
                group, created = Group.objects.get_or_create(name='Visitor')
                user.groups.add(group)
                # Log in the user after registration if needed
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                logging.debug(f"Username: {username}, Password: {password}")
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    logging.debug("User logged in successfully")
                    return redirect('initial-landing')  # Redirect to a success page
                else:
                    logging.error("Authentication failed")  # Log authentication failure
                    return HttpResponseServerError("Authentication failed")  # Return an error response
    except Exception as e:
        logging.error(f"An exception occurred during registration: {str(e)}")  # Log the exception
        return HttpResponseServerError("An error occurred during registration")  # Return an error response

    # If the registration process was not successful, return the registration form
    form = RegistrationForm()
    return render(request, 'unrce/register.html', {'form': form})


@login_required
def profile(request):
    try:
        user = request.user  # Assuming you are using Django's authentication system
        account = Account.objects.get(user=user)  # Retrieve the Account associated with the user
    except Account.DoesNotExist:

        account = None
    return render(request, 'unrce/profile.html', {'user': user, 'account': account})

def must_be_signed_in(request):
    return render(request, 'unrce/redirect.html')


@login_required
def edit_reporting(request):
    return render(request, 'unrce/report_list.html')


@login_required
def org_eoi(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        organization = request.POST.get('organization')
        message = request.POST.get('message')


        subject = 'Expression of Interest'
        email_message = f'Username: {username}\nOrganization: {organization}\nMessage: {message}'


        send_mail(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            ['miltonyong@gmail.com'],  # OWNER EMAIL
            fail_silently=False,
        )
        return redirect('success_page')
    return render(request, 'unrce/organization_eoi.html')

@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def approve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.approved = True
    report.save()
    return redirect('report_details', report_id=report_id)

@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def change_group(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        group_id = request.POST.get('group')
        group = get_object_or_404(Group, id=group_id)
        user.groups.clear()  # Remove user from all current groups
        user.groups.add(group)  # Add user to the selected group
        user.save()
    return redirect('users_list')
