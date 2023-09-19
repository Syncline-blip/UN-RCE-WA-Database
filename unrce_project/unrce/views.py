from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ReportForm, RegistrationForm, ExcelForm, InterestForm, ReportImagesForm
from .models import Report, Account, ReportImages, Expression_of_interest
from django.http import HttpResponseServerError  # Import HttpResponseServerError for error responses
import os
import pandas as pd
import logging

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
def create_report(request): 
    return render(request, 'unrce/create_report.html')

@login_required
def projects(request):
    context = {
        'project': project
    }
    return render(request, 'unrce/project_upload.html', context)
# Create your views here.

@login_required
def add_report(request):
    """
    Handles the creation of a new report and its associated images.
    """
    if request.method == 'POST':
        report_form = ReportForm(request.POST)
        images_form = ReportImagesForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')

        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.author = request.user
            report.save()
    
            if images:  # Check if any images are uploaded
                for image in images:
                    ReportImages.objects.create(
                        report=report,
                        image=image
                    )
            return redirect('report_list')

    else:
        report_form = ReportForm()
        images_form = ReportImagesForm()
    context = {
        'report_form': report_form,
        'images_form': images_form
    }

    return render(request, 'unrce/create_report.html', context)


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


def report_edit(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()

        # Handle new image uploads
        images = request.FILES.getlist('image')
        for image in images:
            ReportImages.objects.create(
                report=report,
                image=image
            )

        return redirect('report_list')  # Redirect to the list of reports
    else:
        form = ReportForm(instance=report)

    existing_images = ReportImages.objects.filter(report=report)
    context = {
        'form': form,
        'existing_images': existing_images,
    }
    return render(request, 'unrce/report_edit.html', context)

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

@login_required
def upload_excel(request):
    """
    Handles the upload of an Excel file for mass creation of Report objects.
    Validates the uploaded file through ExcelForm, reads the Excel file using Pandas,
    iterates through its rows to create Report objects, and then redirects to the home page.
    """
    if request.method == 'POST':
        form = ExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file_instance = form.save()
            # Read Excel File
            df = pd.read_excel(excel_file_instance.excel_file.path)
            # Process and Save Data
            for index, row in df.iterrows():
                Report.objects.create(
                    lead_organisation=row[0],
                    name_project=row[1],
                    project_description = row[2],
                    delivery = row[3],
                    frequency = row[4],
                    audience = row[5],
                    current_partners = row[6],
                    sdg_focus = row[7],
                    contact = row[7],
                    author=request.user
                )
            os.remove(excel_file_instance.excel_file.path)
            return redirect('/')
    else:
        form = ExcelForm()
    return render(request, 'unrce/excel_upload.html', {'form': form})


