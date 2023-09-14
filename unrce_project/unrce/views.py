from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ReportForm, RegistrationForm, ExcelForm, ReportImageFormSet
from .models import Report, Account, ReportImages
from django.http import HttpResponseServerError  # Import HttpResponseServerError for error responses
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

def forms(request): 
    return render(request, 'unrce/forms.html')


def create_report(request): 
    return render(request, 'unrce/create_report.html')


def projects(request):
    context = {
        'project': project
    }
    return render(request, 'unrce/project_upload.html', context)
# Create your views here.

def add_report(request):
    if request.method == 'POST':
        report_form = ReportForm(request.POST)
        formset = ReportImageFormSet(request.POST, request.FILES, queryset=ReportImages.objects.none())
        
        if report_form.is_valid() and formset.is_valid():
            report = report_form.save(commit=False)
            report.author = request.user
            report.save()

            for form_data in formset:
                image = form_data.cleaned_data.get('image')
                if image:
                    ReportImages.objects.create(image=image, report=report)
            return redirect('report_list')
    else:
        report_form = ReportForm()
        formset = ReportImageFormSet(queryset=ReportImages.objects.none())

    return render(request, 'unrce/create_report.html', {'form': report_form, 'formset': formset})




def report_list(request):
    reports = Report.objects.filter(author=request.user)
    return render(request, 'unrce/report_list.html', {'reports': reports})

def report_review(request):
    reports = Report.objects.filter()
    return render(request, 'unrce/report_review.html', {'reports': reports})

def report_edit(request, report_id):
    report = get_object_or_404(Report, id = report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'unrce/report_edit.html', {'form': form})

def register(request):
    try:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                logging.debug("Form is valid")
                user = form.save()
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



def profile(request):
    user = request.user  # Assuming you are using Django's authentication system
    account = Account.objects.get(user=user)  # Retrieve the Account associated with the user
    return render(request, 'unrce/profile.html', {'user': user, 'account': account})

def edit_reporting(request):
    return render(request, 'unrce/report_list.html')
def reportDetails(request):
    return render(request, 'unrce/report_details.html')

def upload_excel(request):
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
            
            return redirect('/')
    else:
        form = ExcelForm()
    
    return render(request, 'unrce/excel_upload.html', {'form': form})


