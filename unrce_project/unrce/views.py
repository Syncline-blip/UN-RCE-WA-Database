from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ReportForm, RegistrationForm
from .models import Report
from django.http import HttpResponseServerError  # Import HttpResponseServerError for error responses

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
    return render(request, 'unrce/home_landing.html')

def projects(request):
    context = {
        'project': project
    }
    return render(request, 'unrce/project_upload.html', context)
# Create your views here.

def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            form.save()
            return redirect('/')  
    else:
        form = ReportForm()

    return render(request, 'unrce/report_form.html', {'form': form})

def report_list(request):
    reports = Report.objects.all()
    return render(request, 'unrce/report_list.html', {'reports': reports})

def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk)
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
                    return redirect('profile')  # Redirect to a success page
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
    return render(request, 'unrce/profile.html')