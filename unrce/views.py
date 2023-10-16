# Standard library imports
import logging
import csv

# Third-party imports
import pandas as pd
from django.conf import settings
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied


# Local application/library specific imports
from .forms import (AccountForm, EditProfileForm, InterestForm, OrganizationInlineFormSet,
                    ReportFilesForm, ReportForm, ReportImagesForm, RegistrationForm)
from .models import (Account, AUDIENCE_CHOICES, DELIVERY_CHOICES,
                     FREQUENCY_CHOICES, Report, ReportFiles, ReportImages, themes_esd,
                     priority_action_areas)





logger = logging.getLogger(__name__)
# sample data, not to be used, just for testing
project = [
    {
        'author': 'JOHN JOHN',
        'project': 'PROJECT LIVE',
        'project_code': 22341
    }
]
# Renders the home page
def home(request):
    return render(request, 'unrce/initial-landing.html')

# Checks if the logged-in user is an admin
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

# Checks if the logged-in user is a member or an admin
def is_member(user):
    return user.groups.filter(name='Member').exists() or is_admin(user)

# Checks if the logged-in user is a visitor, member, or an admin
def is_visitor(user):
    return user.groups.filter(name='Visitor').exists() or is_member(user) or is_admin(user)

# This view is responsible for creating a report; only accessible to members or admins
@login_required
@user_passes_test(is_member,login_url=reverse_lazy('initial-landing'))
def create_report(request): 
    """
    This is where the reports are created that are saved in the database, handles all the fields
    that are needed and returns them in forms
    """
    try:
    
        if request.method == 'POST':
            # Instantiate forms with POST data and FILES
            report_form = ReportForm(request.POST)
            images_form = ReportImagesForm(request.POST, request.FILES)
            files_form = ReportFilesForm(request.POST, request.FILES)
            organization_formset = OrganizationInlineFormSet(request.POST)
            images = request.FILES.getlist('image')
            files = request.FILES.getlist('file')
            
            # Processing selected SDGs 
            direct_sdgs = []
            indirect_sdgs = []
            for i in range(1, 18):
                option = request.POST.get(f'sdg_option_{i}')
                if option == 'direct':
                    direct_sdgs.append(str(i))
                elif option == 'indirect':
                    indirect_sdgs.append(str(i))

            # Processing selected ESD themes
            direct_esd = []
            indirect_esd = []
            for theme in themes_esd:
                option = request.POST.get(f'esd_theme_option_{theme}')
                if option == 'direct':
                    direct_esd.append(theme)
                elif option == 'indirect':
                    indirect_esd.append(theme)
            
            # Processing selected priority areas
            direct_priority = []
            indirect_priority = []
            for area in priority_action_areas:
                option = request.POST.get(f'esd_priority_option_{area}')
                if option == 'direct':
                    direct_priority.append(area)
                elif option == 'indirect':
                    indirect_priority.append(area)
            
            # If all forms are valid, save the report and associated data
            if report_form.is_valid() and organization_formset.is_valid():
                report = report_form.save(commit=False)
                report.author = request.user
                report.direct_sdgs = direct_sdgs  
                report.indirect_sdgs = indirect_sdgs 
                report.direct_esd_themes = direct_esd  
                report.indirect_esd_themes = indirect_esd
                report.direct_priority_areas = direct_priority
                report.indirect_priority_areas = indirect_priority
                if 'submit_for_approval' in request.POST:
                    report.submitted = True
                report.save()
                
                #Handle the Organization formset
                organization_formset = OrganizationInlineFormSet(request.POST, instance=report)
                if organization_formset.is_valid():
                    organization_formset.save()
                report_form.save_m2m()  
                
                #Image handling
                if images:
                    for image in images:
                        ReportImages.objects.create(
                            report=report,
                            image=image
                        )
                
                #File handling
                if files:
                    for file in files:
                        ReportFiles.objects.create(
                            report=report,
                            file=file
                        )

                return redirect('report_list')
            #Logging errors
            else:
                for form in [report_form, images_form, files_form, organization_formset]:
                    if not form.is_valid():
                        logger.error(f'{form.__class__.__name__} errors: {form.errors}')
        #Handle get requests
        else:
            report_form = ReportForm()
            images_form = ReportImagesForm()
            files_form= ReportFilesForm()
            report = Report()
            organization_formset = OrganizationInlineFormSet(instance=report)

        #Preparing SDG numbers for list
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
    Handles the Expression of Interest form submission. 
    It initializes and validates the InterestForm and, if valid, associates 
    the current user as the author, saves the form, and redirects to the initial landing page.
    """
    # Handle POST request, meaning the form has been submitted
    if request.method == 'POST':
        Interest_Form = InterestForm(request.POST)

        # If the form is valid, save it and associate the current user as the author
        if Interest_Form.is_valid():
            interest = Interest_Form.save(commit=False)
            interest.author = request.user
            interest.save()

            # Redirect to the initial landing page after saving the form
            return redirect('initial-landing')

    # If it's a GET request, provide an empty form for the user to fill out
    else:
        Interest_Form = InterestForm()

    # Render the page with the form
    return render(request, 'unrce/eoi.html', {'form': Interest_Form})


def contact(request):
    return render(request, 'unrce/contact.html')


@login_required
@user_passes_test(is_member, login_url=reverse_lazy('initial-landing'))
def report_list(request):
    """
    Lists all reports created by the currently logged-in user.
    The user must be logged in and belong to the 'member' or 'admin' group to view this page.
    """
    # Fetch all reports authored by the current user
    reports = Report.objects.filter(author=request.user)

    # Render the report list page with the user's reports
    return render(request, 'unrce/report_list.html', {'reports': reports})


def browse_reports(request):
    """
    Displays all approved reports, allowing users to filter reports 
    based on certain criteria like status, region, frequency, and audience.
    """
    # Collect filters from the GET request parameters
    filters = {
        'status': request.GET.get('statusFilter'),
        'region': request.GET.get('regionFilter'),
        'frequency': request.GET.get('frequencyFilter'),
        'approved': True
    }

    # Apply audience filter if present in the GET request parameters
    audience_filter = request.GET.getlist('audienceFilter')
    if audience_filter:
        filters['audience__overlap'] = audience_filter

    # Remove any filters that are not set (i.e., are None)
    filters = {k: v for k, v in filters.items() if v}

    # Fetch reports that match the filters
    approved_reports = Report.objects.filter(**filters)

    # Apply SDG filter if present in the GET request parameters
    sdg_filter = request.GET.getlist('sdgFilter')
    if sdg_filter:
        q_objects = Q()

        # Create Q objects for each SDG filter selected by the user
        for sdg in sdg_filter:
            q_objects |= Q(direct_sdgs__contains=[sdg]) | Q(indirect_sdgs__contains=[sdg])

        # Filter the queryset with the OR'ed Q objects
        approved_reports = approved_reports.filter(q_objects)

    # Prepare the context with SDGs and filtered reports, and render the page
    context = {
        'sdgs': range(1, 18),
        'reports': approved_reports
    }

    return render(request, 'unrce/browse_reports.html', context)

@login_required
@user_passes_test(is_member, login_url=reverse_lazy('initial-landing'))
def delete_image(request, image_id):
    """
    Allows a user to delete an image from a report. The user must be logged in and 
    either a member or an admin. The user can only delete images from their own reports.
    """
    # Retrieve the image by ID or return a 404 error if not found
    image = get_object_or_404(ReportImages, id=image_id)
    
    # Ensure the request user is the author of the report containing the image
    if image.report.author == request.user:
        image.delete()

    # Redirect to the report edit page
    return redirect('report_edit', report_id=image.report.id)

@login_required
@user_passes_test(is_member, login_url=reverse_lazy('initial-landing'))
def delete_file(request, file_id):
    """
    Allows a user to delete a file attached to a report. The user must be logged in and 
    either a member or an admin. The user can only delete files from their own reports.
    """
    # Retrieve the file by ID or return a 404 error if not found
    file = get_object_or_404(ReportFiles, id=file_id)
    
    # Ensure the request user is the author of the report containing the file
    if file.report.author == request.user:
        file.delete()

    # Redirect to the report edit page
    return redirect('report_edit', report_id=file.report.id)


@login_required
@user_passes_test(is_admin, login_url=reverse_lazy('initial-landing'))
def users_list(request):
    """
    Lists all users for admins. Admins can search for users by username, 
    first name, last name, email, or organization. Displays all users if no search term is provided.
    """
    # Extract the search query from the GET parameters
    query = request.GET.get('q') 

    # If a search query is provided, filter users based on the search term
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(account__organization__icontains=query)
        ).prefetch_related('groups', 'account')

    # If no search query is provided, return all users
    else:
        users = User.objects.all().prefetch_related('groups', 'account')

    # Create the context dictionary to provide data to the template
    context = {
        'users': users,
        'all_groups': Group.objects.all()
    }

    # Render the users list page with the context
    return render(request, 'unrce/users_list.html', context)


@login_required
@user_passes_test(is_admin, login_url=reverse_lazy('initial-landing'))
def report_review(request):
    """
    Allows administrators to review all reports submitted in the system. Admins can 
    view all reports, irrespective of the author, for the purpose of review.
    """
    # Retrieve all reports
    reports = Report.objects.all()
    
    # Render the report review page with the list of reports
    return render(request, 'unrce/report_review.html', {'reports': reports})

def report_details(request, report_id):
    """
    Displays the detailed view of a specific report for review. The detailed view includes 
    all the information and files associated with the report.
    """
    # Retrieve the specific report by ID or return a 404 error if not found
    report = get_object_or_404(Report, id=report_id)
    
    # Create a form instance to display the report details
    report_form = ReportForm(instance=report)
    
    # Retrieve associated images and files for the report
    existing_images = ReportImages.objects.filter(report=report)
    existing_files = ReportFiles.objects.filter(report=report)
    
    # Create a context dictionary to hold all data to be displayed in the template
    context = {
        'form': report_form, 
        'existing_images': existing_images,
        'report': report,
        'existing_files': existing_files
    }
    
    # Render the report details page with the context
    return render(request, 'unrce/report_details.html', context)


@login_required
@user_passes_test(is_member,login_url=reverse_lazy('initial-landing'))
def report_edit(request, report_id):
    """
    Allows the member to edit their own report. This view enables members to update
    the report fields, including attached images and files.
    """
    report = get_object_or_404(Report, id=report_id)
    if report.author != request.user and not request.user.groups.filter(name='Admin').exists():
        raise PermissionDenied

    # Ensure the request.user is the author of the report or has permission

    try:
        if request.method == 'POST':
            # Getting list of uploaded images and files
            report_form = ReportForm(request.POST, instance=report)
            images_form = ReportImagesForm(request.POST, request.FILES)
            files_form = ReportFilesForm(request.POST, request.FILES)
            organization_formset = OrganizationInlineFormSet(request.POST, instance=report)
            images = request.FILES.getlist('image')
            files = request.FILES.getlist('file')
            if 'submit_for_approval' in request.POST:
                report.submitted = True

            # If both report form and organization formset are valid, proceed with saving
            if report_form.is_valid() and organization_formset.is_valid():
                report = report_form.save(commit=False)  

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

                if 'submit_for_approval' in request.POST:
                    report.submitted = True
                    report.save()

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

        # Handling the GET request to render the edit page with initial data
        else:
            report_form = ReportForm(instance=report)
            images_form = ReportImagesForm()
            files_form = ReportFilesForm()
            organization_formset = OrganizationInlineFormSet(instance=report)
        
        # Preparing context data for rendering the template
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
    """
    Displays the profile of the currently logged-in user.
    It fetches the associated Account object for additional user details.
    If the Account object does not exist, it sets the account to None.
    Renders the 'unrce/profile.html' template.
    """
    try:
        user = request.user  
        account = Account.objects.get(user=user)  
    except Account.DoesNotExist:
        account = None
    
    return render(request, 'unrce/profile.html', {'user': user, 'account': account})


@login_required
def edit_reporting(request):
    return render(request, 'unrce/report_list.html')



@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def approve_report(request, report_id):
    """
    Allows an admin to approve a report.
    Fetches the report by ID, sets its 'approved' attribute to True, and saves the update.
    Redirects to the report details page to view the approved report.
    """
    report = get_object_or_404(Report, id=report_id)
    report.approved = True
    report.save()
    return redirect('report_details', report_id=report_id)

@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def change_group(request, user_id):
    """
    Allows an admin to change the group of a specific user.
    If the request method is POST, it captures the selected group from the request,
    removes the user from all current groups, and adds the user to the selected group.
    Redirects to the users list page to view the update.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        group_id = request.POST.get('group')
        group = get_object_or_404(Group, id=group_id)
        user.groups.clear()  # Remove user from all current groups
        user.groups.add(group)  # Add user to the selected group
        user.save()
    
    return redirect('users_list')



@login_required
def edit_profile(request):
    """
    Allows the logged-in user to edit their own profile.
    Handles both the GET and POST methods. 
    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)

            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if new_password and new_password == confirm_password:
                user.set_password(new_password)

            user.save()

            if new_password:
                update_session_auth_hash(request, user)  # Updates the session hash to keep the user authenticated

            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def membership_request(request):
    """
    Handles membership requests.
    Logged-in users can request for membership by filling out the form.
    """
    try:
        # Try to get the existing account for the logged-in user
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        # If account does not exist, then create a new one
        account = None
    
    if request.method == 'POST':
        if account:
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)
            
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.requesting = True 
            new_account.save()
            return redirect('initial-landing')
    else:
        if account:
            form = AccountForm(instance=account)
        else:
            form = AccountForm()

    return render(request, 'unrce/membership_request.html', {'form': form})

@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def approve_membership(request, account_id):
    """
    Allows an admin to approve membership requests.
    Fetches the Account by ID, marks it as approved, adds the user to the Member group, 
    and redirects to the membership review page.
    """
    account = get_object_or_404(Account, id=account_id)
    account.approved = True
    account.requesting = False  
    member_group = Group.objects.get(name='Member')
    account.user.groups.add(member_group)
    account.save()
    return redirect('membership_review')

@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def membership_review(request):
    """
    Displays a list of all membership requests for admin review.
    Fetches all accounts where requesting is True and approved is False, and renders them for review.
    """
    accounts = Account.objects.select_related('user').filter(requesting=True, approved=False)

    return render(request, 'unrce/membership_review.html', {'accounts': accounts})

@require_POST
@csrf_protect
@login_required
@user_passes_test(is_member,login_url=reverse_lazy('initial-landing'))
def report_delete(request, id):
    """
    Allows a member to delete a specific report by ID.
    Fetches the report by ID, deletes it, and redirects to the report list page.
    The function is protected against CSRF attacks and requires the user to be a member.
    """
    report = get_object_or_404(Report, id=id)
    report.delete()
    return redirect('report_list') 


@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def download_reports(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports.csv"'

    writer = csv.writer(response)

    # Write your header names here
    writer.writerow([
        'Report ID', 'Title of Project', 'Delivery', 'Frequency', 'Web Link',
        'Additional Resources', 'Region', 'Ecosystem', 'Audience',
        'Socio-Economic Characteristics', 'Development Challenges',
        'Sustainable Development Policy', 'Status', 'Start Project',
        'End Project', 'Rationale', 'Objectives', 'Activities/Practices',
        'Size Academic', 'Results', 'Lessons Learned', 'Key Message',
        'Relationship Activities', 'Funding', 'Created At', 'Last Modified',
        'Author', 'Approved', 'Submitted', 'Direct SDGs', 'Indirect SDGs',
        'Direct ESD Themes', 'Indirect ESD Themes', 'Direct Priority Areas',
        'Indirect Priority Areas'
    ])

    reports = Report.objects.all()

    for report in reports:
        writer.writerow([
            report.id, report.title_project, ', '.join(report.delivery) if report.delivery else '',
            report.frequency, report.web_link, report.additional_resources, report.region, 
            report.ecosystem, ', '.join(report.audience) if report.audience else '',
            report.socio_economic_characteristics, report.development_challenges,
            report.sustainable_development_policy, report.status, report.start_project,
            report.end_project, report.rationale, report.objectives, report.activities_practices,
            report.size_academic, report.results, report.lessons_learned, report.key_message,
            report.relationship_activities, report.funding, report.created_at, report.last_modified,
            report.author, report.approved, report.submitted, ', '.join(map(str, report.direct_sdgs)) if report.direct_sdgs else '',
            ', '.join(map(str, report.indirect_sdgs)) if report.indirect_sdgs else '', 
            ', '.join(report.direct_esd_themes) if report.direct_esd_themes else '',
            ', '.join(report.indirect_esd_themes) if report.indirect_esd_themes else '', 
            ', '.join(report.direct_priority_areas) if report.direct_priority_areas else '',
            ', '.join(report.indirect_priority_areas) if report.indirect_priority_areas else ''
        ])

    return response

@login_required
@user_passes_test(is_admin,login_url=reverse_lazy('initial-landing'))
def download_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    
    # Write headers to CSV file
    writer.writerow([
        "User ID", "Username", "First Name", "Last Name", "Email",
        "Organization", "Profile SDG", "Sector", "Approved", "Requesting", "Message"
    ])
    
    # Query all users
    users = User.objects.all()
    
    for user in users:
        writer.writerow([
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            user.email,
            user.account.organization if hasattr(user, 'account') else '',
            ', '.join(user.account.profile_sdg) if hasattr(user, 'account') else '',
            user.account.sector if hasattr(user, 'account') else '',
            user.account.approved if hasattr(user, 'account') else '',
            user.account.requesting if hasattr(user, 'account') else '',
            user.account.message if hasattr(user, 'account') else '',
        ])
    
    return response