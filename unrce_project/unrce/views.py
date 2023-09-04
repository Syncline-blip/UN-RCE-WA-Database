from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ReportForm
from .forms import UserCreationForm
from .models import Report

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

def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            return redirect('/')  
    else:
        form = ReportForm()

    return render(request, 'unrce/create_report.html', {'form': form})

def report_list(request):
    reports = Report.objects.filter(author=request.user)
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

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            return redirect('home_landing')
    else:
        form = UserCreationForm()
    
    return render(request, 'unrce/sign_up.html', {'form': form})