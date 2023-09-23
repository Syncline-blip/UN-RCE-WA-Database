from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ReportForm, RegistrationForm, InterestForm, ReportImagesForm, ReportFilesForm, OrganizationInlineFormSet
from .models import Report, Account, ReportImages, Expression_of_interest, ReportFiles, AUDIENCE_CHOICES, DELIVERY_CHOICES, FREQUENCY_CHOICES
from django.http import HttpResponseServerError, JsonResponse  
import os, json
import pandas as pd
import logging
from django.db.models import Q

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


@login_required
def create_report(request, report_id=None): 
    is_editing = True if report_id else False

    if is_editing:
        report = get_object_or_404(Report, id=report_id)
        direct_sdgs = report.direct_sdgs
        indirect_sdgs = report.indirect_sdgs
        linked_users = report.linked_users.all()
    else:
        report = Report()
        direct_sdgs = []
        indirect_sdgs = []
        linked_users = []

    try:
        if request.method == 'POST':
            report_form = ReportForm(request.POST, instance=report)
            images_form = ReportImagesForm(request.POST, request.FILES)
            files_form = ReportFilesForm(request.POST, request.FILES)
            organization_formset = OrganizationInlineFormSet(request.POST, instance=report)
            images = request.FILES.getlist('image')
            files = request.FILES.getlist('file')
            
            new_direct_sdgs = []
            new_indirect_sdgs = []
            for i in range(1, 18):
                option = request.POST.get(f'sdg_option_{i}')
                if option == 'direct':
                    new_direct_sdgs.append(str(i))
                elif option == 'indirect':
                    new_indirect_sdgs.append(str(i))

            direct_sdgs = new_direct_sdgs
            indirect_sdgs = new_indirect_sdgs



            if report_form.is_valid() and organization_formset.is_valid():
                report = report_form.save(commit=False)
                report.author = request.user
                report.direct_sdgs = direct_sdgs  
                report.indirect_sdgs = indirect_sdgs 
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
                if not report_form.is_valid():
                    logger.error(f'ReportForm errors: {report_form.errors}')
                    if not images_form.is_valid():
                        logger.error(f'ReportImagesForm errors: {images_form.errors}')
                        if not files_form.is_valid():
                            logger.error(f'ReportFilesForm errors: {files_form.errors}')
                            if not organization_formset.is_valid():
                                logger.error(f'OrganizationInlineFormSet errors: {organization_formset.errors}')
        else:
            report_form = ReportForm(instance=report if is_editing else None)
            images_form = ReportImagesForm()
            files_form= ReportFilesForm()
            organization_formset = OrganizationInlineFormSet(instance=report, queryset=report.organization_set.all())


        sdg_list = [str(i) for i in range(1, 18)]
        context = {
            'report_form': report_form,
            'organization_formset': organization_formset,
            'images_form': images_form,
            'files_form': files_form,
            'sdg_list': sdg_list,
            'selected_direct_sdgs': direct_sdgs,
            'selected_indirect_sdgs': indirect_sdgs,
            'linked_users': linked_users,
            'all_users': User.objects.all(),
            'is_editing': is_editing
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




@login_required
def report_list(request):
    """
    Lists all the Report objects authored by the currently logged-in user.
    Fetches and filters the Report objects by the current user and renders them in 'unrce/report_list.html'.
    """
    reports = Report.objects.filter(author=request.user)
    return render(request, 'unrce/report_list.html', {'reports': reports})

@login_required
def delete_image(request, image_id):
    """
    Allows users to delete images they have uploaded to reports
    """
    image = get_object_or_404(ReportImages, id=image_id)
    report = image.report
    if image.report.author == request.user:
        image.delete()
    return redirect('report_edit', report_id=report.id)

def users_list(request):
    users = User.objects.all().prefetch_related('groups', 'account')  
    context = {
        'users': users,
    }
    return render(request, 'unrce/users_list.html', context)

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
        'existing_images': existing_images
    }
    return render(request, 'unrce/report_details.html', context)

def eoi_review(request):
    """
    Lists all the Report objects available in the system, without filtering by author.
    Fetches all the Report objects and renders them in 'unrce/report_review.html'.
    """
    eois = Expression_of_interest.objects.filter()
    return render(request, 'unrce/eoi_review.html', {'eois': eois})



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
def reportDetails(request):
    return render(request, 'unrce/report_details.html')

